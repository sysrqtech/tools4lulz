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

import os
import time
import vk


class SysRq(Exception):
    pass


class SleepAPI(vk.API):
    """
    Prevent from 'Too many requests per second' error
    """

    def __getattr__(self, method_name):
        time.sleep(0.33)
        return vk.API.__getattr__(self, method_name)


def resolve(url, *, wall=False):
    """
    Resolving some details about VK page by screen name
    :param url: screen name or URL
    :param wall: if True, function will return wall id
    :return: {"id": wall_id, "name": screen_name,
              "title": title, "type": wall_type}
    """
    wall_data = api.utils.resolveScreenName(screen_name=url.split("/")[-1])
    if not wall_data:
        raise SysRq("Неверный URL")
    wall_type = wall_data["type"]
    obj_id = wall_data["object_id"]

    if wall_type in ["group", "page"]:
        group_data = api.groups.getById(group_ids=obj_id)[0]
        screen_name = group_data["screen_name"]
        title = group_data["name"]
        if wall:
            wall_id = "-" + str(obj_id)
        else:
            wall_id = obj_id
    else:
        profile = api.users.get(user_ids=obj_id, fields="screen_name")[0]
        screen_name = profile["screen_name"]
        title = "{first_name} {last_name}".format(**profile)
        wall_id = obj_id
    return {"id": wall_id, "name": screen_name,
            "title": title, "type": wall_type}


def make_packs(l, num, *, fixed_value=True):
    if not fixed_value:
        pack_len = len(l) // num
    else:
        pack_len = num
    work_list = l.copy()
    result = []
    while work_list:
        list_slice = work_list[:pack_len]
        if list_slice:
            result.append(list_slice)
        del work_list[:pack_len]
    if work_list:
        result.append(work_list)
    return result


def percents(el, seq):
    if isinstance(seq, int):
        percent = int(el) * 100 / seq
    else:
        percent = (seq.index(el) + 1) * 100 / len(seq)
    return round(percent, 2)


def list_of_str(seq):
    return [str(el) for el in seq]


api = SleepAPI(vk.Session(), v="5.53")
user_agent = {"User-Agent":
              "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
app_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
static = os.path.join(app_root, "static")
