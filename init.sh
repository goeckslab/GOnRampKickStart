#!/usr/bin/env bash

# install roles
ansible-galaxy install -r requirements_roles.yml -p roles

# make role modifications
\cp -r modified_roles/* roles/
