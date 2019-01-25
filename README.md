# GOnRampKickStart
An Ansible-driven deployment script for [G-OnRamp](http://g-onramp.org), a [Galaxy](https://galaxyproject.org)-based platform that creates genome browsers for any eukaryotic genome, and allows their [collaborative annotation with Apollo](http://genomearchitect.github.io/). Adapted from [GalaxyKickStart](https://github.com/ARTBio/GalaxyKickStart).

Requires:
- [`ansible` version >= 2.2](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [`git` version >= 2.11](https://git-scm.com/downloads)
- a valid target (remote or local system, VM, container, ...)

## Usage:
1. [Configure `gonramp_inventory` file](#configure-gonramp_inventory-file)
2. [Run `kickstart.sh`](#run-kickstartsh)
3. [Wait...](#wait)
4. [More info](#more-info)

## Configure `gonramp_inventory` file
While [the file itself contains basic examples](https://github.com/goeckslab/GOnRampKickStart/blob/master/gonramp_inventory), more reading can be found in [Ansible's documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html). The target system *must be running Ubuntu 16.04*.

## Run `kickstart.sh`
From the terminal, execute:
```
$ ./kickstart.sh <options>
```

This downloads required Ansible roles, ensures everything is versioned and configured correctly, then runs against a target specified in the `gonramp_inventory` file.

optional options:
- `-t "<comma seperated tags>"` **OR** `-s "<comma seperated tags>"`
  - whatever tags are in the quotation marks will be given to [ansible's tag options](https://docs.ansible.com/ansible/latest/user_guide/playbooks_tags.html) (`-t` to include ONLY those tags, `-s` to skip ONLY those tags)
- `-v N` where 0 > N > 5 (1 2 3 or 4)
  - this sets Ansible's verbosity level; `-v 4` is maximally verbose
- `-i`
  - this flag just installs the dependencies to run the full G-OnRamp playbook, but does not execute the playbook
  
## Wait...
per the script:
```
[G-OnRamp] Installing G-OnRamp ...
WARNING! This will take some time (multiple hours)
```

## More info
[Deployment options at our website under 'Getting Started with G-OnRamp'](http://gonramp.wustl.edu/#sow-editor-3)
