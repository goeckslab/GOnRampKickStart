#!/usr/bin/env python
"""converts a tool dictionary into string yaml-formatted"""
#exceptions
EXCEPTIONS = ["regtools_junctions_extract"]

def tool_to_yaml(tool_dict, label, tool_deps=True, rep_deps=True, res_deps=True):
    """a function that creates a yaml entry for a particular set of Galaxy tools"""
    priority_tools = ['regtools_junctions_extract', 'jbrowsearchivecreator']
    names = priority_tools
    # set global defaults
    yml = "\
install_tool_dependencies: "+str(tool_deps)+"\n\
install_repository_dependencies: "+str(rep_deps)+"\n\
install_resolver_dependencies: "+str(res_deps)+"\n\n\
tools:"
    for name in tool_dict:
        names = names + [name] if name not in names else names
    for name in names:
        if name in tool_dict and "tool_shed" in tool_dict[name]:
            tool = tool_dict[name]
        else:
            continue
        yml += "\n- name: " + name
        yml += "\n  owner: " + tool["owner"]
        yml += "\n  revisions:"
        for rev in tool["revisions"]:
            yml += "\n  - " + rev
        yml += "\n  tool_panel_section_label: " + label
        yml += "\n  tool_shed_url: " + tool["tool_shed"]
        if name in EXCEPTIONS:
            yml += "\n  install_resolver_dependencies: False"
    return yml + "\n"
