import sys

import setup


def hook(config):
    if sys.version_info[0] < 3:
        sys.path.insert(0, setup.PY2K_DIR)
