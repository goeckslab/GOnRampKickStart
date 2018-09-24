#!/usr/bin/env python
import argparse
from bioblend import galaxy
from bioblend import ConnectionError as BBConnectionError

PARSER = argparse.ArgumentParser(description='Install Galaxy tool list.')

REQUIRED = PARSER.add_argument_group('required named arguments')

REQUIRED.add_argument('-a', type=str, help='address of target host', required=True)
REQUIRED.add_argument('-k', type=str, help='API key for Galaxy instance', required=True)
ARGS = PARSER.parse_args()

TC= galaxy.tools.ToolClient(galaxy.GalaxyInstance(url=ARGS.a, key=ARGS.k))

# get the tools
for t in TC.get_tools():
    print("  getting deps for: {}".format(t["id"]))
    try:
        TC.install_dependencies(t["id"])
    # some strange access error based on trying to update baked-in tools
    except BBConnectionError as err:
        if err.status_code == 401:
            print("\t\t- dependency unavailable")
            continue
        else:
            raise err
