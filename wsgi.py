#!/usr/bin/env python
# coding=utf-8

# This file may be used instead of Apache mod_wsgi to run your python
# web application in a different framework.

import imp
import os
import sys

try:
    virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR', '.'), 'virtenv')
    python_version = "python" + str(sys.version_info[0]) + "." + str(sys.version_info[1])
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib', python_version, 'site-packages')
    virtualenv = os.path.join(virtenv, 'bin', 'activate_this.py')
    exec(open(virtualenv).read(), dict(__file__=virtualenv))
except IOError:
    pass

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

application = app = imp.load_source('app', '__init__.py')
