#!/usr/local/bin/python-odoo-shell
from odoo.tools import config
assert config.get("limit_request") == 9000
assert not config.get("list_db")
