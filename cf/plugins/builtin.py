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

"""Builtin plugins"""

import logging

from cf.filter.exportfilter import CSVExportFilter
try:
    import ooolib
except ImportError:
    pass
else:
    from cf.filter.exportfilter import OOCalcExportFilter
try:
    import xlwt
except ImportError, err:
    pass
else:
    from cf.filter.exportfilter import XlsExportFilter

try: from cf.db.backends.mysql import MySQL
except ImportError, err:
    logging.warning('Could not import MySQLBackend: %s', err)
try: from cf.db.backends.oracle import Oracle
except ImportError, err:
    logging.warning('Could not import OracleBackend; %s', err)

from cf.shell import CFShell
from cf.library import SQLLibraryPlugin
from cf.nativeshell import NativeShellPlugin

