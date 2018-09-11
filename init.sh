#!/usr/bin/env bash

# install roles
ansible-galaxy install -r requirements_roles.yml -p roles

# check if modifications needed
\cp -r modified_roles/* roles/
