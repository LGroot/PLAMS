#!/usr/bin/env python

from scm.plams import *

plams_namespace = globals().copy()

VERSION = 1.2

import argparse
import os
import shutil
import sys
import threading
import traceback
from os.path import join as opj

parser = argparse.ArgumentParser(description='PLAMS environment execution tool ("master script")')
parser.add_argument('--version', action='version', version='PLAMS '+str(VERSION), help='show version number and exit')
parser.add_argument('-p', '--path', type=str, default=None, help='place where the main working folder is created', metavar='path', dest='path')
parser.add_argument('-f', '--folder', type=str, default=None, help='name of the main working folder', metavar='name', dest='folder')
parser.add_argument('-v', '--var',  action='append', type=str, default=[], help="declare a variable 'var' with a value 'value' in the global namespace. Multiple variables can be set this way, but each one requires a separate '-v'", metavar='var=value', dest='vars')
parser.add_argument('-l', '--load', action='append', type=str, default=[], help="load all jobs from the given location before executing the script. Multiple paths can be given, but each one requires a separate '-l'", metavar='path', dest='load')
parser.add_argument('-r', '--restart', action='store_true', help='perform a restart run (import all jobs from the folder given by -f argument and use the same folder for the current run)', dest='restart')
parser.add_argument('file', nargs='+', type=str, help='file with PLAMS script')
args = parser.parse_args()


#add -v variables to the plams_namespace
for pair in args.vars:
    if '=' in pair:
        var, val = pair.split('=')
        plams_namespace[var] = val


#read and concatenate input file(s)
inputscript = ''
for input_file in args.file:
    if os.path.isfile(input_file):
        with open(input_file, 'r') as f:
            inputscript += f.read()
    else:
        print('Error: File %s not found' % input_file)
        sys.exit(1)


#handle restart
restart_backup = None
if args.restart:
    if args.folder:
        restartdir = opj(args.path, args.folder) if args.path else args.folder
        if os.path.isdir(restartdir):
            if os.listdir(restartdir):
                restart_backup = restartdir + '.res'
                n = 1
                while os.path.exists(restart_backup):
                    n += 1
                    restart_backup = restartdir + '.res' + str(n)
                os.rename(restartdir, restart_backup)
                args.load.append(restart_backup)
        else:
            print('WARNING: The folder specified for restart does not exist. Ignoring -r flag.')
    else:
        print('WARNING: To perform a restart run you need to specify the folder with -f flag. Ignoring -r flag.')


#initialize PLAMS (normpath prevents crash when f ends with /)
init(path=args.path, folder=args.folder)

#write down input script
with open(config.jm.input, 'w') as f:
    f.write(inputscript)

#load jobs from -l folders
for path in args.load:
    load_all(path)

#execute input script
try:
    exec(compile(open(config.jm.input).read(), config.jm.input, 'exec'), plams_namespace)
except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    tb = traceback.extract_tb(exc_tb)
    fname, lineno, fn, text = tb[-1]
    err_msg = 'Execution interrupted by the following exception:\n'
    err_msg += '%s: %s\n' % (exc_type.__name__, str(e))
    err_msg += 'File: %s\n' % os.path.basename(fname)
    err_msg += 'Line %i: %s\n\n' % (lineno, text)
    err_msg += '==============Full traceback========================'
    for fname, lineno, fn, text in tb:
        err_msg += '\nFile: %s' % os.path.basename(fname)
        err_msg += '\nLine %i: %s' % (lineno, text)
        err_msg += '\n----------------------------------------------------'
    log(err_msg)

#clean the environment
finish()
if restart_backup:
    shutil.rmtree(restart_backup)

