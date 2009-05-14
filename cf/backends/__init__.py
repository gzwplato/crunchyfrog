# -*- coding: utf-8 -*-

# crunchyfrog - a database schema browser and query tool
# Copyright (C) 2008 Andi Albrecht <albrecht.andi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Database backends"""

import sys
import time

import gobject
import gtk

from cf.utils import Emit


class DBFeatures(object):
    """Defines available database features."""
    transactions = False


class DBConnection(gobject.GObject):

    __gsignals__ = {
        "closed" : (gobject.SIGNAL_RUN_LAST,
                    gobject.TYPE_NONE,
                    tuple()),
        "notice" : (gobject.SIGNAL_RUN_LAST,
                    gobject.TYPE_NONE,
                    (str,)),
    }

    __gproperties__ = {
        "transaction-state" : (gobject.TYPE_PYOBJECT,
                            "Transaction flag", "Transaction flag",
                            gobject.PARAM_READWRITE),
    }

    def __init__(self, provider, app):
        self.app = app
        self.provider = provider
        self.datasource_info = None
        self.conn_number = None
        self.threadsafety = 0
        self.coding_hint = "utf-8"
        self._transaction_state = TRANSACTION_IDLE
        self.__gobject_init__()

    @property
    def db_id(self):
        # Propagate datasource info's db id.
        if self.datasource_info is None:
            return None
        return self.datasource_info.db_id

    def do_set_property(self, property, value):
        if property.name == "transaction-state":
            self._transaction_state = value
        else:
            raise AttributeError, "unknown property %r" % property.name

    def do_get_property(self, property):
        if property.name == "transaction-state":
            return self._transaction_state
        else:
            raise AttributeError, "unknown property %r" % property.name

    def get_label(self, short=False):
        if short:
            prefix = _(u'Connection')
        else:
            prefix = self.datasource_info.get_label()
        return prefix + " #%s" % self.conn_number

    def close(self):
        self.emit("closed")

    def cursor(self):
        raise NotImplementedError

    def update_transaction_status(self):
        pass

    def get_server_info(self):
        return None

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def explain(self, statement):
        return []


class DBCursor(gobject.GObject):

    def __init__(self, connection):
        self.connection = connection
        self.__gobject_init__()

    def execute(self, query):
        raise NotImplementedError

    def get_messages(self):
        return []

    def close(self):
        raise NotImplementedError

    def prepare_statement(self, sql):
        """Prepare statement for execution.

        This method could be overwritten by backend implementations
        to prepare a statement before it's execute with this cursor.

        The default implementation just returns the given statement.
        """
        return sql



