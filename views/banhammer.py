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

from flask import Blueprint, request, redirect, url_for, render_template, make_response, current_app

try:
    from ..modules import banhammer
except ValueError:
    from modules import banhammer

banhammer_view = Blueprint('banhammer', __name__)


@banhammer_view.route('/list')
def list_banned():
    return render_template("banhammer/banhammer_list.html", db=banhammer.list_db())


@banhammer_view.route('/check')
def check_banned():
    return banhammer.check(request.args["id"])


@banhammer_view.route('/ban', methods=["POST"])
def ban():
    links = request.form["link"].strip().split("\n")
    reason = request.form["reason"].strip()
    auth_hash = request.form["hash"]
    moderator = request.form["name"]
    return banhammer.ban(links, reason, hash=auth_hash, moderator=moderator)


@banhammer_view.route('/unban', methods=["POST"])
def unban():
    link = request.form["link"]
    auth_hash = request.form["hash"]
    return banhammer.unban(link, auth_hash)


@banhammer_view.route('/')
def ban_page():
    auth_hash = request.cookies.get("hash")
    name = request.cookies.get("name")
    if auth_hash in banhammer.hashes:
        return render_template("banhammer/index.html", auth_hash=auth_hash, name=name)
    elif current_app.debug:
        return render_template("banhammer/index.html", auth_hash=banhammer.hashes[0], name="Cyber Tailor")
    else:
        raise banhammer.BanhammerError("Хеши расходятся")


@banhammer_view.route('/auth', methods=["POST"])
def post_auth():
    auth_hash = request.args["hash"]
    name = request.args["first_name"] + " " + request.args["last_name"]
    if auth_hash in banhammer.hashes:
        response = make_response(redirect(url_for("banhammer")))
        response.set_cookie("hash", auth_hash)
        response.set_cookie("name", name)
        return response
    else:
        return auth_hash


@banhammer_view.route('/login')
def auth():
    return render_template("banhammer/auth.html")
