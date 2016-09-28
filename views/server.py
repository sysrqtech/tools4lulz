# coding=utf-8

"""
Copyright © 2016, Matvey Vyalkov

This file is part of SysRq tools4lulz.
SysRq tools4lulz is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SysRq tools4lulz is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with SysRq tools4lulz.  If not, see <http://www.gnu.org/licenses/>.
"""

import traceback
import json
from flask import Blueprint, request, render_template, send_from_directory
from werkzeug.exceptions import InternalServerError

server_view = Blueprint('server', __name__)


@server_view.app_errorhandler(500)
def internal_server_error(error: InternalServerError, tb):
    error_message = str(error)
    error_class = repr(error.__class__())[:-2]
    error_msg = "{}: {}".format(error_class, error_message)
    log = "".join(traceback.format_tb(tb)).replace("\n", "<br>").replace(" ", "&nbsp;")
    return render_template("500.html", text=error_msg, log=log), 500


@server_view.route('/')
def index():
    return render_template('index.html')


@server_view.route('/favicon.ico')
def get_favicon():
    return server_static('img/favicon.ico')


@server_view.route('/<path:resource>')
def server_static(resource):
    return send_from_directory('static/', resource)


@server_view.route('/update')
def check():
    program = request.args["program"] or "all"
    if program == "all":
        return json.load("static/db/versions.json")
    else:
        return json.load("static/db/versions.json")
