#!/usr/bin/env python
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
import os; print(os.getcwd()); exit()
import sys
import configparser

from flask import Flask, got_request_exception
from raven.contrib.flask import Sentry
from werkzeug.exceptions import InternalServerError

try:
    from .views import server
    from .views import banhammer
    from .views import vk_utils
    from .views import ipg
except SystemError:
    from views import server
    from views import banhammer
    from views import vk_utils
    from views import ipg


def reraise(value, tb=None):
    if value.__traceback__ is not tb:
        raise value.with_traceback(tb)
    raise value


class TracebackFlask(Flask):
    def handle_exception(self, e):
        """
        Default exception handling that kicks in when an exception
        occurs that is not caught.  In debug mode the exception will
        be re-raised immediately, otherwise it is logged and the handler
        for a 500 internal server error is used.  If no such handler
        exists, a default 500 internal server error message is displayed.
        """
        exc_type, exc_value, tb = sys.exc_info()

        got_request_exception.send(self, exception=e)
        handler = self._find_error_handler(InternalServerError())

        if self.propagate_exceptions:
            # if we want to repropagate the exception, we can attempt to
            # raise it with the whole traceback in case we can do that
            # (the function was actually called from the except part)
            # otherwise, we just raise the error again
            if exc_value is e:
                reraise(exc_value, tb)
            else:
                raise e

        self.log_exception((exc_type, exc_value, tb))
        if handler is None:
            return InternalServerError()
        return handler(e, tb)  # don't forget traceback argument in your handler!


app = TracebackFlask(__name__)
app.config.from_pyfile('flask.cfg')

config = configparser.ConfigParser()
config.read("tools4lulz.ini")

sentry_dsn = config["sentry"]["dsn"]
if not app.debug:
    sentry = Sentry(app, dsn=sentry_dsn)

# registering modules
app.register_blueprint(server.server_view)
app.register_blueprint(banhammer.banhammer_view, url_prefix="/banhammer")
app.register_blueprint(vk_utils.vk_view, url_prefix="/vk")
app.register_blueprint(ipg.ipg_view, url_prefix="/ipg")


if __name__ == '__main__':
    app.run(app.config['IP'], app.config['PORT'])
