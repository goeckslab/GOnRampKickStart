[![Build Status](https://travis-ci.org/ARTbio/GalaxyKickStart.svg?branch=master)](https://travis-ci.org/ARTbio/GalaxyKickStart)

# G-OnRamp Kick-Start

G-OnRamp Kick-Start is a fork of  [GalaxyKickStart](https://github.com/ARTbio/GalaxyKickStart), "an [Ansible playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) designed to help you get one or more production-ready  [Galaxy](https://galaxyproject.org/) servers based on Ubuntu within minutes, and to maintain these servers".

### Getting Started ###


### Required Ansible version >= 2.4

GalaxyKickStart has been developed at the [ARTbio platform](http://artbio.fr)
and contains roles developed by the [Galaxy
team](https://github.com/galaxyproject/).

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
