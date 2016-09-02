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

import json
import os

from . import general

hashes = ["9e8789399618fd70882e9b7690c26413",
          "7508ed607cdeef9ce75c91494d9935f0",
          "a39b8c4fc3cede81adc5da5eac497ae9",
          "b488651b907cf9afd047207b894c7432",
          "28ac9f68d72b91498074aed37731a7df"]


class BanhammerError(Exception):
    pass


class BannedDB:
    def __init__(self, filename):
        self.filename = filename
        self.content = {}
        if not os.path.isfile(self.filename):
            self._dump()
        else:
            self._reload()

    def __contains__(self, key):
        return str(key) in self.content

    def _reload(self):
        self.content = json.load(open(self.filename))

    def _dump(self):
        with open(self.filename, "w") as db:
            json.dump(self.content, db)
        self._reload()

    def add(self, user):
        self.content.update(user)
        self._dump()

    def remove(self, user_id):
        self.content.pop(str(user_id))
        self._dump()

    def list(self):
        return self.content.items()

    def ban(self, link, reason, moderator):
        """
        Ban single user.
        :param link
        :param reason
        :param moderator
        :return: message to display
        """
        user_id = general.api.utils.resolveScreenName(screen_name=link.split("/")[-1])["object_id"]
        name = "{first_name} {last_name}".format(**general.api.users.get(user_ids=user_id)[0])
        if user_id not in self:
            self.add({user_id: {"reason": reason, "name": name, "banner": moderator}})
            return "Пользователь {} забанен".format(name)
        return "Пользователь {} уже забанен".format(name)

    def unban(self, link):
        """
        Unban single user.
        :param link
        :return: message to display
        """
        user_id = general.api.utils.resolveScreenName(screen_name=link.split("/")[-1])["object_id"]
        name = "{first_name} {last_name}".format(**general.api.users.get(user_ids=user_id)[0])
        if user_id in self:
            self.remove(user_id)
            return "Пользователь {} разбанен".format(name)
        return "Пользователь {} не забанен".format(name)


def ban(db: BannedDB, links: list, reason, *, hash, moderator):
    """
    Ban some users at one time.
    :param links
    :param reason
    :param hash: md5(app_id+user_id+secret_key)
    :param moderator
    :return: message do display
    """
    if hash not in hashes:
        return "Операция не позволена"
    if len(links) == 1:
        return db.ban(links[0], reason, moderator)
    else:
        for link in links:
            db.ban(link, reason, moderator)
        return "Пользователи забанены"


def unban(db: BannedDB, links: list, hash):
    """
    Unban some users at one time.
    :param links
    :param hash: md5(app_id+user_id+secret_key)
    :return: message to display
    """
    if hash not in hashes:
        raise BanhammerError("Операция не позволена")
    if len(links) == 1:
        return db.unban(links[0])
    else:
        for link in links:
            db.unban(link)
        return "Пользователи разбанены"
