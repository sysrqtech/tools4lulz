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

from flask import Blueprint, render_template, request

try:
    from ..modules import ipg
except ValueError:
    from modules import ipg

ipg_view = Blueprint('ipg', __name__)


@ipg_view.route('/picturer/gen', methods=["POST"])
def ipg_gen():
    link = request.form["link"]
    message = request.form["message"]
    size = request.form["size"] if request.form["size"] else 0
    align = request.form["align"]
    mark = bool(request.form["watermark"])
    return ipg.ipg_build(link, message, size, align, mark)


@ipg_view.route('/picturer')
def ipg_picturer():
    return render_template("ipg/picturer.html")
