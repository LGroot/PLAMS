import numpy as np
from scm.csh import CSHessian

from ..core.basejob import MultiJob
from ..core.errors import JobError
from ..core.results import Results
from ..interfaces.adfsuite.adf import ADFJob
from ..tools.units import Units


__all__ = ['CSHessianADFJob', 'CSHessianADFResults']


class CSHessianADFResults(Results):
    def get_hessian(self):
        return self.hessians[-1]


class CSHessianADFJob(MultiJob):
    _result_type = CSHessianADFResults

    def __init__(self, molecule, basistype, displacement=0.01, start=0.2, step=1, **kwargs):
        MultiJob.__init__(self, children={}, **kwargs)
        self.molecule = molecule
        self.basistype = basistype
        self.disp = displacement
        self.start = start
        self.step = step


    def prerun(self):
        self.restartjob = ADFJob(name=self.name+'_res', molecule=self.molecule, settings=self.settings.gradient)
        self.restartjob.parent = self
        self.restartjob.run()

        self.N = 3 * len(self.molecule)
        self.perm = np.random.permutation(self.N)
        self.pick = int(self.N * self.start)
        self.batch = self.perm[:self.pick]

        self.basis = self.get_basis(self.basistype)
        self.csh = CSHessian(self.basis)
        self.samp = self.csh.get_sampling_basis()

        self.scaling = [None] * self.N
        self.results.hessians = []
        for i in self.batch:
            for step in [-1,1]:
                self.children[(i, step)] = self.create_forces_job(i, step)


    def create_forces_job(self, column, step):
        vec = self.samp[:, column]
        vec.shape = (-1,3)

        #scale vec in such a way that most displaced atom is moved by self.disp
        max_displ = 0.0
        for v in vec:
            max_displ = max(max_displ, np.linalg.norm(v))
        self.scaling[column] = self.disp / max_displ

        mol = self.molecule.copy()
        for at, v in zip(mol, vec):
            at.translate(self.scaling[column] * step * v)

        newjob = ADFJob(name=f'{self.name}_{column}_{step}', molecule=mol, settings=self.settings.gradient)
        newjob.settings.input.restart.file = self.restartjob
        newjob.settings.input.restart.nogeo = 'True'
        return newjob


    def get_basis(self, arg):
        if isinstance(arg, str):
            if arg in self.settings.basis:
                s = self.settings.basis[arg]
                self.basisjob = s.jobtype(name=self.name+'_basis', molecule=self.molecule, settings=s)
                self.basisjob.parent = self
                self.basisjob.run()
                hess = s.get_hessian(self.basisjob.results)
                hess.shape = (self.N, self.N)

            elif arg is 'cart':
                return np.eye(self.N)

            else:
                raise JobError(f"CSHessianADFJob: I don't understand 'basistype={arg}' argument. My Settings should contain .basis.{arg} branch, but they do not.")

        else:
            try:
                arg = np.array(arg)
                arg.shape = (self.N, self.N)
            except:
                raise JobError(f"CSHessianADFJob: argument supplied as 'basistype' cannot be transformed into numpy array of size ({self.N},{self.N})")
            return arg

        evals, evecs = np.linalg.eigh(hess)
        return evecs


    def new_batch(self):
        self.pick += self.step
        return self.perm[self.pick-self.step : self.pick]


    def new_children(self):
        for i in self.batch:
            v1 = np.array(self.children[(i,-1)].results.readkf('GeoOpt', 'Gradients_InputOrder'))
            v2 = np.array(self.children[(i,1)].results.readkf('GeoOpt', 'Gradients_InputOrder'))
            grad_cart = Units.convert(v2 - v1, 'bohr', 'angstrom') / (2*self.scaling[i])
            grad_samp = np.dot(self.samp.T, grad_cart)
            self.csh.add_column(i, grad_samp)
        self.results.hessians.append(self.csh.estimate())

        self.batch = self.new_batch()
        ret = {}
        for i in self.batch:
            for step in [-1,1]:
                ret[(i,step)] = self.create_forces_job(i, step)
        return ret


