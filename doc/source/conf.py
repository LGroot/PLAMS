# -*- coding: utf-8 -*-
#
# PLAMS documentation build configuration file, created by
# sphinx-quickstart2 on Mon Aug 11 16:40:00 2014.

import sys
import os
from datetime import date

from docutils.parsers.rst.directives.admonitions import Important,Danger,Attention
from sphinx.locale import admonitionlabels

admonitionlabels['important'] = 'Technical'
admonitionlabels['danger'] = 'Warning'

def modify_signature(app, what, name, obj, options, signature,
                           return_annotation):
    if signature:
        signature = signature.replace("=u'","='")
    return signature, return_annotation

def setup(app):
    if not tags.has('scm_theme'):
        app.add_stylesheet('boxes.css')
    app.add_directive('warning', Danger)
    app.add_directive('technical', Important)
    app.connect('autodoc-process-signature', modify_signature)


# ==================================================================================
# If we build from the userdoc, we should use the configuration from global_conf.py,
# otherwise we should define a fall-back config for the stand-alone plams doc.
# ==================================================================================

if tags.has('scm_theme'):

    from global_conf import *
    project, htmlhelp_basename, latex_documents = set_project_specific_var ('PLAMS')

else:

    extensions = []

    # Add any paths that contain templates here, relative to this directory.
    templates_path = ['_templates']

    # The suffix of source filenames.
    source_suffix = '.rst'

    # The master toctree document.
    master_doc = 'index'

    # General information about the project.
    project = u'PLAMS'
    copyright = u'%i, Software for Chemistry & Materials'%(date.today().year)

    # The version info for the project you're documenting, acts as replacement for
    # |version| and |release|, also used in various other places throughout the
    # built documents.
    #
    # The short X.Y version.
    version = '1.3'
    # The full version, including alpha/beta/rc tags.
    #release = ''

    # The language for content autogenerated by Sphinx. Refer to documentation
    # for a list of supported languages.
    #language = None

    # There are two options for replacing |today|: either, you set today to some
    # non-false value, then it is used:
    #today = ''
    # Else, today_fmt is used as the format for a strftime call.
    #today_fmt = '%B %d, %Y'

    # List of patterns, relative to source directory, that match files and
    # directories to ignore when looking for source files.
    exclude_patterns = []

    # The reST default role (used for this markup: `text`) to use for all
    # documents.
    #default_role = None

    # If true, '()' will be appended to :func: etc. cross-reference text.
    add_function_parentheses = True

    # A list of ignored prefixes for module index sorting.
    #modindex_common_prefix = []

    # If true, keep warnings as "system message" paragraphs in the built documents.
    #keep_warnings = False

    # -- Options for HTML output ----------------------------------------------

    # The theme to use for HTML and HTML Help pages.  See the documentation for
    # a list of builtin themes.
    html_theme = 'classic'

    # Theme options are theme-specific and customize the look and feel of a theme
    # further.  For a list of options available for each theme, see the
    # documentation.
    html_theme_options = {
        "collapsiblesidebar": "true",
        "externalrefs": "true"
    }

    # Add any paths that contain custom themes here, relative to this directory.
    #html_theme_path = []

    # The name for this set of Sphinx documents.  If None, it defaults to
    # "<project> v<release> documentation".
    html_title = 'PLAMS documentation'

    # A shorter title for the navigation bar.  Default is the same as html_title.
    #html_short_title = 'PLAMS'

    # The name of an image file (relative to this directory) to place at the top
    # of the sidebar.
    html_logo = '_static/plams_logo.png'

    # The name of an image file (within the static path) to use as favicon of the
    # docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
    # pixels large.
    html_favicon = '_static/favicon.ico'

    # Add any paths that contain custom static files (such as style sheets) here,
    # relative to this directory. They are copied after the builtin static files,
    # so a file named "default.css" will overwrite the builtin "default.css".
    html_static_path = ['_static']

    # Add any extra paths that contain custom files (such as robots.txt or
    # .htaccess) here, relative to this directory. These files are copied
    # directly to the root of the documentation.
    #html_extra_path = []

    # If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
    # using the given strftime format.
    #html_last_updated_fmt = '%b %d, %Y'

    # If true, SmartyPants will be used to convert quotes and dashes to
    # typographically correct entities.
    #html_use_smartypants = True

    # Custom sidebar templates, maps document names to template names.
    #html_sidebars = {}

    # Additional templates that should be rendered to pages, maps page names to
    # template names.
    #html_additional_pages = {}

    # If false, no module index is generated.
    #html_domain_indices = True

    # If false, no index is generated.
    #html_use_index = True

    # If true, the index is split into individual pages for each letter.
    #html_split_index = False

    # If true, links to the reST sources are added to the pages.
    html_show_sourcelink = True

    # If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
    html_show_sphinx = False

    # If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
    #html_show_copyright = True

    # If true, an OpenSearch description file will be output, and all pages will
    # contain a <link> tag referring to it.  The value of this option must be the
    # base URL from which the finished HTML is served.
    #html_use_opensearch = ''

    # This is the file name suffix for HTML files (e.g. ".xhtml").
    #html_file_suffix = None

    # Output file base name for HTML help builder.
    htmlhelp_basename = 'PLAMSdoc'


# ==================================================================================
# Common stuff for both scm_theme and "native" build
# ==================================================================================


extensions += [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode']

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'python3': ('http://docs.python.org/3.6', None)}

autodoc_default_flags = ['members', 'private-members', 'special-members']
autodoc_member_order = 'bysource'

rst_epilog = """
.. |init| replace:: :func:`~scm.plams.core.functions.init`
.. |log| replace:: :func:`~scm.plams.core.functions.log`
.. |load| replace:: :func:`~scm.plams.core.functions.load`
.. |load_all| replace:: :func:`~scm.plams.core.functions.load_all`
.. |finish| replace:: :func:`~scm.plams.core.functions.finish`
.. |add_to_class| replace:: :func:`~scm.plams.core.functions.add_to_class`
.. |add_to_instance| replace:: :func:`~scm.plams.core.functions.add_to_instance`

.. |PlamsError| replace:: :exc:`~scm.plams.core.errors.PlamsError`
.. |FileError| replace:: :exc:`~scm.plams.core.errors.FileError`
.. |ResultsError| replace:: :exc:`~scm.plams.core.errors.ResultsError`
.. |PTError| replace:: :exc:`~scm.plams.core.errors.PTError`
.. |UnitsError| replace:: :exc:`~scm.plams.core.errors.UnitsError`
.. |MoleculeError| replace:: :exc:`~scm.plams.core.errors.MoleculeError`

.. |Job| replace:: :class:`~scm.plams.core.basejob.Job`
.. |SingleJob| replace:: :class:`~scm.plams.core.basejob.SingleJob`
.. |MultiJob| replace:: :class:`~scm.plams.core.basejob.MultiJob`
.. |run| replace:: :meth:`~scm.plams.core.basejob.Job.run`
.. |get_input| replace:: :meth:`~scm.plams.core.basejob.SingleJob.get_input`
.. |get_runscript| replace:: :meth:`~scm.plams.core.basejob.SingleJob.get_runscript`
.. |prerun| replace:: :meth:`~scm.plams.core.basejob.Job.prerun`
.. |postrun| replace:: :meth:`~scm.plams.core.basejob.Job.postrun`
.. |load_external| replace:: :meth:`~scm.plams.core.basejob.SingleJob.load_external`

.. |Atom| replace:: :class:`~scm.plams.mol.atom.Atom`
.. |Bond| replace:: :class:`~scm.plams.mol.bond.Bond`
.. |Molecule| replace:: :class:`~scm.plams.mol.molecule.Molecule`

.. |PeriodicTable| replace:: :class:`~scm.plams.tools.periodic_table.PeriodicTable`
.. |Units| replace:: :class:`~scm.plams.tools.units.Units`

.. |JobManager| replace:: :class:`~scm.plams.core.jobmanager.JobManager`
.. |load_job| replace:: :meth:`~scm.plams.core.jobmanager.JobManager.load_job`

.. |JobRunner| replace:: :class:`~scm.plams.core.jobrunner.JobRunner`
.. |GridRunner| replace:: :class:`~scm.plams.core.jobrunner.GridRunner`

.. |Settings| replace:: :class:`~scm.plams.core.settings.Settings`
.. |Results| replace:: :class:`~scm.plams.core.results.Results`
.. |KFReader| replace:: :class:`~scm.plams.tools.kftools.KFReader`
.. |KFFile| replace:: :class:`~scm.plams.tools.kftools.KFFile`

.. |AMSJob| replace:: :class:`~scm.plams.interfaces.adfsuite.ams.AMSJob`
.. |AMSResults| replace:: :class:`~scm.plams.interfaces.adfsuite.ams.AMSResults`

.. |ADFJob| replace:: :class:`ADFJob<scm.plams.interfaces.adfsuite.adf.ADFJob>`
.. |ADFResults| replace:: :class:`ADFResults<scm.plams.interfaces.adfsuite.adf.ADFResults>`

.. |SCMJob| replace:: :class:`~scm.plams.interfaces.adfsuite.scmjob.SCMJob`
.. |SCMResults| replace:: :class:`~scm.plams.interfaces.adfsuite.scmjob.SCMResults`

.. |BANDJob| replace:: :class:`BANDJob<scm.plams.interfaces.adfsuite.band.BANDJob>`
.. |BANDResults| replace:: :class:`BANDResults<scm.plams.interfaces.adfsuite.band.BANDResults>`

.. |DFTBJob| replace:: :class:`DFTBJob<scm.plams.interfaces.adfsuite.dftb.DFTBJob>`
.. |DFTBResults| replace:: :class:`DFTBResults<scm.plams.interfaces.adfsuite.dftb.DFTBesults>`

.. |MOPACJob| replace:: :class:`~scm.plams.interfaces.adfsuite.mopac.MOPACJob`
.. |MOPACResults| replace:: :class:`~scm.plams.interfaces.adfsuite.mopac.MOPACResults`

.. |ReaxFFJob| replace:: :class:`~scm.plams.interfaces.adfsuite.reaxff.ReaxFFJob`
.. |ReaxFFResults| replace:: :class:`~scm.plams.interfaces.adfsuite.reaxff.ReaxFFResults`

.. |UFFJob| replace:: :class:`~scm.plams.interfaces.adfsuite.uff.UFFJob`
.. |UFFResults| replace:: :class:`~scm.plams.interfaces.adfsuite.uff.UFFResults`

.. |DensfJob| replace:: :class:`~scm.plams.interfaces.adfsuite.densf.DensfJob`
.. |DensfResults| replace:: :class:`~scm.plams.interfaces.adfsuite.densf.DensfResults`

.. |FCFJob| replace:: :class:`~scm.plams.interfaces.adfsuite.fcf.FCFJob`
.. |FCFResults| replace:: :class:`~scm.plams.interfaces.adfsuite.fcf.FCFResults`

.. |DiracJob| replace:: :class:`~scm.plams.interfaces.dirac.DiracJob`
.. |DiracResults| replace:: :class:`~scm.plams.interfaces.dirac.DiracResults`

.. |CrystalJob| replace:: :class:`CrystalJob<scm.plams.interfaces.thirdparty.crystal.CrystalJob>`
.. |mol2CrystalConf| replace:: :func:`mol2CrystalConf<scm.plams.interfaces.thirdparty.crystal.mol2CrystalConf>`

.. |Cp2kJob| replace:: :class:`Cp2kJob<scm.plams.interfaces.thirdparty.cp2k.Cp2kJob>`
.. |Cp2kResults| replace:: :class:`Cp2kJob<scm.plams.interfaces.thirdparty.cp2k.Cp2kResults>`

.. |DFTBPlusJob| replace:: :class:`~scm.plams.interfaces.thirdparty.dftbplus.DFTBPlusJob`
.. |DFTBPlusResults| replace:: :class:`~scm.plams.interfaces.thirdparty.dftbplus.DFTBPlusResults`

.. |VibrationsJob| replace:: :class:`~scm.plams.recipes.vibration.VibrationsJob`
.. |IRJob| replace:: :class:`~scm.plams.recipes.vibration.IRJob`
.. |VibrationsResults| replace:: :class:`~scm.plams.recipes.vibration.VibrationsResults`

.. |RPM| replace:: :ref:`rerun-prevention`
.. |cleaning| replace:: :ref:`cleaning`
.. |pickling| replace:: :ref:`pickling`
.. |restarting| replace:: :ref:`restarting`
.. |master-script| replace:: :ref:`master-script`
.. |binding_decorators| replace:: :ref:`binding-decorators`
.. |parallel| replace:: :ref:`parallel`

.. |nbsp| unicode:: 0xA0
   :trim:
"""

