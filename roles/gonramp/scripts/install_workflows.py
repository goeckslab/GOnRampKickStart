#!/usr/bin/env python
"""a module to install Galaxy workflows (and optionally tools)"""
import datetime
import argparse

from os.path import isfile, join, exists
from os import listdir
import ast
from subprocess import call

from bioblend import galaxy

#local imports
from tool_to_yaml import tool_to_yaml

#-------------------------------------------------------------------
#   Argument enumeration and parsing
PARSER = argparse.ArgumentParser(description='Install Galaxy workflows')
# required arguments
REQUIRED = PARSER.add_argument_group('required named arguments')
REQUIRED.add_argument('-a', type=str,\
                      help="the address of the target host running Galaxy", required=True)
REQUIRED.add_argument('-k', type=str, help="your Galaxy instance API key", required=True)
# OR arguments: at least one of these is present
PARSER.add_argument('-wl', nargs='+',\
                    help="space-delimited list of workflows to install to host Galaxy")
PARSER.add_argument('-wd', help="directory of workflow files (*.ga) to install to host Galaxy")
# Optional arguments
PARSER.add_argument('-t',\
                    help="flag that indicates tools should be installed from workflows",\
                    action="store_true")

ARGS = PARSER.parse_args()

if ARGS.wl is None and ARGS.wd is None:
    PARSER.error("ERROR: at least one workflow argument (-wl or -wd) is required")

#-------------------------------------------------------------------
#   Instantiate galaxy api objects
GI = galaxy.GalaxyInstance(url=ARGS.a, key=ARGS.k)
WFC = galaxy.workflows.WorkflowClient(GI)

#-------------------------------------------------------------------
#   Helper functions
def verify_list():
    """Create a list of files with .ga extension from supplied list."""
    # install workflows from -wl tag
    if not ARGS.wl:
        return []
    wflows = [wf for wf in ARGS.wl if isfile(wf) and wf[-3:] == ".ga"]
    return wflows

def verify_directory():
    """Create a list of files with .ga extension from supplied directory."""
    # install workflows from -wd tag
    if not ARGS.wd:
        return []
    if not exists(ARGS.wd):
        print("ERROR: " + ARGS.wd + " is not a valid directory")
        return []
    # create list from available .ga files
    return [join(ARGS.wd, wf) for wf in listdir(ARGS.wd) \
            if isfile(join(ARGS.wd, wf)) \
            and wf[-3:] == ".ga"]

def dict_from_file(file_path):
    """extract a dictionary from a given yaml file"""
    with open(file_path, 'r') as raw:
        filestring = raw.read()
        filestring = filestring.replace(": null", ": None")
        result = ast.literal_eval(filestring)
        if isinstance(result, dict):
            return result
    return {}

def process_tool_dict(t_d, current_tool=None):
    """takes a dictionary of workflow steps and adds a new entry"""
    if current_tool is None:
        current_tool = {}
    result = current_tool
    # each step has at most one installable tool
    for step in t_d.keys():
        tool = t_d[step]
        if "tool_shed_repository" in tool:
            tsr = tool["tool_shed_repository"]
            t_name = tsr["name"]
            t_rev = tsr["changeset_revision"]
            if t_name in result.keys():
                if t_rev not in result[t_name]["revisions"]:
                    result[t_name]["revisions"].append(t_rev)
            else:
                result[t_name] = {\
                                 "revisions": [t_rev],\
                                 "owner": tsr["owner"],\
                                 "tool_shed": tsr["tool_shed"]}
    return result

def install_all():
    """Create a union of workflow sources and install them."""
    wf_list = list(set().union(verify_list(), verify_directory()))
    wf_list.sort()

    tools = {}
    for wflow in wf_list:
        WFC.import_workflow_from_local_path(wflow, True)
        if ARGS.t:
            wf_d = dict_from_file(wflow)
            if "steps" in wf_d.keys():
                tool_d = wf_d["steps"]
                tools = process_tool_dict(tool_d, tools)

    if ARGS.t:
	#install tools
        dtime = datetime.datetime.now()
        tmp_file = "/tmp/gtools_"+str(dtime.microsecond)+".yml"
        with open(tmp_file, "w+") as raw:
            raw.write(tool_to_yaml(tools, "G-OnRamp Tools"))
        env = "/usr/bin/env"
        cmd = "/tmp/gonramp/install_tool_yml.py"
        call(["pwd"])
        t_args = ["-a", ARGS.a, "-k", ARGS.k, "-t", tmp_file]
        call([env, "python", cmd] + t_args)
        call([env, "rm", "-f", tmp_file])

        ta_file = "/tmp/gonramp/tool_addenda.yml"
        if isfile(ta_file):
            ta_args = ["-a", ARGS.a, "-k", ARGS.k, "-t", ta_file]
            call([env, "python", cmd] + ta_args)
            call([env, "rm", "-f", ta_file])

#-------------------------------------------------------------------
#   Installation execution
install_all()
