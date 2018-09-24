[![Build Status](https://travis-ci.org/ARTbio/GalaxyKickStart.svg?branch=master)](https://travis-ci.org/ARTbio/GalaxyKickStart)

# G-OnRamp Kick-Start

G-OnRamp Kick-Start is a fork of  [GalaxyKickStart](https://github.com/ARTbio/GalaxyKickStart), "an [Ansible playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) designed to help you get one or more production-ready  [Galaxy](https://galaxyproject.org/) servers based on Ubuntu within minutes, and to maintain these servers".

### Required Ansible version >= 2.4

GalaxyKickStart has been developed at the [ARTbio platform](http://artbio.fr)
and contains roles developed by the [Galaxy
team](https://github.com/galaxyproject/).

### Getting Started ###
To kick-start G-OnRamp:
- Clone this repository, then navigate to it:
```
$ git clone https://github.com/goeckslab/GOnRampKickStart/
cd GOnRampKickStart
```
- run the initialization script to download / modify the roles:
```
$ ./init.sh
```
  - _this downloads required roles and applies any necessary patches_


- edit (_e.g._, with `vim`) your inventory file to point to valid target(s):
```
$ vim inventory_files/gonramp_inventory
```
- run the playbook `gonramp.yml` with ansible
```
$ ansible-playbook -i inventory_files/gonramp_inventory gonramp.yml
```
  - _verbose output can be specified with 1-4 v flags for increasing verbosity_
    - _e.g._ `-v`, `-vv`, `-vvv`, `-vvvv`



List of included external roles:
------
- [ensure_postrgesql_up](https://github.com/ARTbio/ensure_postgresql_up.git)
- [natefoo-postgresql_objects](https://github.com/ARTbio/ansible-postgresql-objects)
- [galaxy-os role](https://github.com/ARTbio/ansible-galaxy-os)
- [galaxy role](https://github.com/ARTbio/ansible-galaxy)
- [miniconda-role](https://github.com/ARTbio/ansible-miniconda-role.git)
- [galaxy-extras role](https://github.com/ARTbio/ansible-galaxy-extras)
- [galaxy-trackster role](https://github.com/galaxyproject/ansible-trackster)
- [galaxy-tools role](https://github.com/ARTbio/ansible-galaxy-tools)

#### G-OnRamp-specific roles ####
- [gonramp role](https://github.com/goeckslab/GOnRampKickStart/tree/master/roles/gonramp)
- [apollo-role](https://github.com/goeckslab/GOnRampKickStart/tree/master/roles/apollo)
- [openjdk-role](https://github.com/goeckslab/GOnRampKickStart/tree/master/roles/openjdk)

#### G-OnRamp Workflows ####
- [G-OnRamp workflow list](https://github.com/goeckslab/GOnRampKickStart/tree/master/roles/gonramp/workflows)
