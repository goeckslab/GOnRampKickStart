#!/usr/bin/env python
"""A module to install tools to a Galaxy instance"""

from time import time, sleep
import sys
import argparse

import yaml

from bioblend import galaxy
from bioblend import ConnectionError as BBConnectionError

#---------------------------------------------------------------
#       Args
PARSER = argparse.ArgumentParser(description='Install Galaxy tool list.')

REQUIRED = PARSER.add_argument_group('required named arguments')

REQUIRED.add_argument('-a', type=str, help='address of target host', required=True)
REQUIRED.add_argument('-k', type=str, help='API key for Galaxy instance', required=True)
REQUIRED.add_argument('-t', type=str, help='yaml file of Galaxy tools', required=True)
ARGS = PARSER.parse_args()

#---------------------------------------------------------------
#       Config
# bioblend default timeout is 5mins from API call
MINUTES = 4 # minutes AFTER bioblend times out
TIMEOUT = 60* (MINUTES + 5) # seconds
SLEEP_TIME = 10 # seconds
BAD_TOOLS = ["regtools_junctions_extract"] # this install can hang indefinitely

#---------------------------------------------------------------
#       Initialize Objects
GI = galaxy.GalaxyInstance(url=ARGS.a, key=ARGS.k)
TSC = galaxy.toolshed.ToolShedClient(GI)
TC = galaxy.tools.ToolClient(GI)

#---------------------------------------------------------------
#       Helper functions
def install_tools_and_deps(tool_list_yaml):
    """Install tools and their dependencies from a provided tool list

    Arguments:
    tool_list_yaml -- a yaml file containing a list of desired tools
    """
    # parse yaml file
    yammy = ""
    with open(tool_list_yaml, 'r') as stream:
        try:
            yammy = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit()

    # for each tool to install, check if it exists; if not, install
    tool_list = list(yammy["tools"])
    for tool in tool_list:
        tool_info = get_tool_info(tool["name"])

        # if there is info, it has been installed to some degree
        if tool_info:
            for rev_idx in range(len(tool["revisions"])):
                revision = tool["revisions"][rev_idx]
                tool_exists = False
                for a_tool in tool_info:
                    if a_tool["changeset_revision"] == revision:
                        print("revision ["+revision+"] installed, moving on...")
                        tool_exists = True
                        break
                if not tool_exists:
                    try_tool(tool, rev_idx)
        else:
            try_tools(tool)

def try_tools(tool):
    """Installs all listed revisions of a tool

    Arguments:
    tool -- a tool from yaml file argument with one or more revisions
    """
    for revision in range(len(tool["revisions"])):
        try_tool(tool, revision)

def try_tool(tool_info, revision_idx=0):
    """Attempt to install a tool, catching any exceptions

    Arguments:
    tool_info -- dict containing extracted information about a single tool
    revision_idx -- the index of the revision in the tool's revision list
    """
    #print("trying {} ... \n\n".format(tool_info))
    elapsed = 0
    start_time = time()
    revision = tool_info["revisions"][revision_idx]
    tool_string = tool_info["name"] + ":" + revision
    print("-Installing " + tool_string + "...")
    print("with tool info {}".format(tool_info))
    try:
        install_tool(tool_info, revision_idx)
    except BBConnectionError as err:
        if err.status_code == 504:
            print("504: connection timed out... checking status of installation")
            while elapsed < TIMEOUT:
                tool_status = get_tool_status(tool_info["name"], revision)
                if tool_info["name"] in BAD_TOOLS:
                    elapsed = time()-start_time
                if tool_status == "Installed":
                    print(tool_string + " installed successfully")
                elif tool_status == "ERROR: NOT FOUND":
                    print("!!ERROR!!: tool not found despite installation attempt.")
                    sys.exit()
                else:
                    sleep(SLEEP_TIME)
            print("!!ERROR!!: " + tool_string + " may not have installed successfully...")
            print("please check tool status (and possibly re-install) \
                  from Galaxy's administration panel")
        return False
    except BaseException as err:
        print("Unexpected Exception: %s"%err)
        print("...exiting...")
        sys.exit()


def install_tool(tool_info, revision_idx):
    """Install the tool specified by tool_info

    Arguments:
    tool_info -- dict containing extracted information about a single tool
    revision_idx -- the index of the revision in the tool's revision list
    """
    install_res_deps = False if tool_info["name"] == "regtools_junctions_extract" \
                       else True
    res = TSC.install_repository_revision(
        tool_shed_url="https://{}".format(tool_info["tool_shed_url"]) if "tool_shed_url" in tool_info else "https://toolshed.g2.bx.psu.edu",
        name=tool_info["name"],
        owner=tool_info["owner"],
        changeset_revision=tool_info["revisions"][revision_idx],
        install_tool_dependencies=True,
        install_repository_dependencies=True,
        install_resolver_dependencies=install_res_deps,
        new_tool_panel_section_label="G-OnRamp Tools")
    return res

def get_tool_info(ident):
    """Get current information of a particular tool
    Arguments:
    ident -- a tool_id string
    """
    result = []
    current_tools = TC.get_tools()
    for tool in current_tools:
        if "tool_shed_repository" in tool and tool["tool_shed_repository"]["name"] == ident:
            insertion = tool["tool_shed_repository"]
            insertion["id"] = tool["id"]
            if tool["tool_shed_repository"] not in result:
                result.append(insertion)
    return result

def get_tool_status(ident, rev):
    """Get current status of a particular tool
    Arguments:
    ident -- a tool_id string
    rev -- tool revision string
    """
    status = TSC.get_repositories()
    for tool in status:
        if tool["name"] == ident and tool["changeset_revision"] == rev:
            return tool["status"]
    return "ERROR: NOT FOUND"

#---------------------------------------------------------------
#       Execute installation
install_tools_and_deps(ARGS.t)
