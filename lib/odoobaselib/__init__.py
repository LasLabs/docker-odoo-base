# -*- coding: utf-8 -*-
import logging
import os
import subprocess

import yaml

# Constants needed in scripts
CUSTOM_DIR = "/opt/odoo/custom"
SRC_DIR = os.path.join(CUSTOM_DIR, 'src')
ADDONS_YAML = os.path.join(SRC_DIR, 'addons')
ADDONS_DIR = "/opt/odoo/auto/addons"
CLEAN = os.environ.get("CLEAN") == "true"
AUTO_REQUIREMENTS = os.environ.get("AUTO_REQUIREMENTS") == "true"
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")
FILE_APT_BUILD = os.path.join(
    CUSTOM_DIR, 'dependencies', 'apt_build.txt',
)

if os.path.isfile('%s.yaml' % ADDONS_YAML):
    ADDONS_YAML = '%s.yaml' % ADDONS_YAML
else:
    ADDONS_YAML = '%s.yml' % ADDONS_YAML

# Customize logging for build
logging.root.name = "docker-odoo-base"
_log_level = os.environ.get("LOG_LEVEL", "")
if _log_level.isdigit():
    _log_level = int(_log_level)
elif _log_level in LOG_LEVELS:
    _log_level = getattr(logging, _log_level)
else:
    if _log_level:
        logging.warning("Wrong value in $LOG_LEVEL, falling back to INFO")
    _log_level = logging.INFO
logging.root.setLevel(_log_level)


def addons_active():
    """ Returns a list of active addons, as defined in `addons.yml`. """
    raw_addons = list(reduce(lambda x, y: x + y, addons_config().values()))
    return list(filter(lambda x: x != '*', raw_addons))


def addons_config():
    """Load configurations from ``ADDONS_YAML`` into a dict."""
    config = dict()
    if not os.path.isfile(ADDONS_YAML):
        return config
    with open(ADDONS_YAML) as addons_file:
        for doc in yaml.load_all(addons_file):
            for repo, addons in doc.items():
                config.setdefault(repo, list())
                config[repo] += addons

    return config


def do_command(command, split=True, shell=False):
    if split:
        command = command.split()
    logging.debug('Running Command: %s', command)
    if shell:
        proc = subprocess.Popen(
            ' '.join(command),
            env=os.environ,
            shell=True,
        )
    else:
        proc = subprocess.Popen(command, env=os.environ)
    proc.communicate()
