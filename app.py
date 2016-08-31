#!/usr/bin/env python
# coding=utf-8

# This file may be used instead of Apache mod_wsgi to run your python
# web application in a different framework.

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

from flask import Flask
from . import app
application = app

# TESTING

if __name__ == '__main__':
    port = app.config['PORT']
    ip = app.config['IP']
    app_name = app.config['APP_NAME']
    host_name = app.config['HOST_NAME']

    print('Starting Flask WSGIServer on %s:%d ... ' % (ip, port))
    server = Flask(__name__)
    server.wsgi_app = app
    server.run(host=ip, port=port)
