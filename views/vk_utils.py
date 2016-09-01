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

import requests
from flask import Blueprint, render_template, request, url_for

try:
    from ..modules import general
    from ..modules import vk_utils
except ValueError:
    from modules import general
    from modules import vk_utils

vk_view = Blueprint('vk', __name__)


@vk_view.route('/resolve')
def resolve_page():
    return render_template("vk/resolve.html")


@vk_view.route('/resolve/result', methods=["POST"])
def resolve_result():
    link = request.form["link"]
    wall = general.resolve(link)
    if wall["type"] in ["group", "page"]:
        return "[club{id}|{title}]".format(**wall)
    else:
        return "[id{id}|{title}]".format(**wall)


@vk_view.route('/anticheat/oauth')
def anticheat_oauth():
    data = requests.get("https://oauth.vk.com/access_token?client_id=5489908" +
                        "&client_secret=l4Hn8Rs2lLn754kxm93h" +
                        "&redirect_uri=" + url_for("vk.anticheat_oauth", _external=True) +
                        "&code=" + request.args["code"]).json()
    token = data["access_token"]
    return render_template("vk/anticheat/set_token.html", token=token)


@vk_view.route('/anticheat/results', methods=["POST"])
def anticheat_results():
    link = request.form["link"]
    token = request.form["token"]
    return render_template("vk/anticheat/chart.html",
                           **vk_utils.anticheat(link, token))


@vk_view.route('/anticheat')
def anticheat():
    return render_template("vk/anticheat/index.html")
