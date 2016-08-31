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

import vk

from . import general


def anticheat(link, token):
    session = vk.Session(token)
    api = general.SleepAPI(session, v="5.53")
    post = link.split("wall")[-1]
    if post == link:
        raise general.SysRq("Ссылка не является постом")
    owner = post.split("_")[0]
    media = api.wall.getById(posts=post)[0]["attachments"]
    try:
        poll = [attach["poll"] for attach in media if "poll" in attach][0]
    except KeyError:
        raise general.SysRq("Опрос не найден")
    answers = [[answer["id"], answer["text"]] for answer in poll["answers"]]
    data = []
    for answer_id, text in answers:
        voters = api.execute.getVoters(owner_id=owner, poll_id=poll["id"], answer_id=answer_id)
        in_group = []
        for pack in general.make_packs(voters, 500):
            in_group.extend(api.groups.isMember(group_id=owner[1:], user_ids=",".join(general.list_of_str(pack))))
        # noinspection PyTypeChecker
        honest_voters = len([user["user_id"] for user in in_group
                             if int(user["member"]) == 1])
        data.append([text, honest_voters])
    votes_sum = sum([variant[1] for variant in data])
    [item.append(str(general.percents(item[1], votes_sum)) + "%") for item in data]
    return dict(data=str(data),
                height=str(100 * len(data)))
