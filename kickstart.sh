
#!/usr/bin/env bash
RED='\033[0;31m'
NC='\033[0m'

SECONDS=0

PFX="[G-OnRamp]"

TRANSPORT_CFG_LINE="transport = paramiko"

WORKFLOWS=https://github.com/goeckslab/G-OnRamp-workflows
EXTRACT_DIR=G-OnRamp-workflows-master

GKS_SHA_PIN=e7dd64b6bc35400fa41e2dec18a68c55d0beb128 #fc5050fd0665f16526e802a4aca207daa6a68b5b
SHALLOW_SINCE=2018-09-01

SHALLOW="--shallow-since=$SHALLOW_SINCE"

function usage
{
  echo "usage:"
  echo -e "  $0 -t \"comma,seperated,tags\""
  echo -e "\t\t\tOR"
  echo -e "  $0 -s \"comma,seperated,tags\""
  echo -e "\t-t: tags to run, to the exclusion of all other tags"
  echo -e "\t-s: tags to skip, running all other tags"
  echo -e "\t\tnote: these options are mutually exclusive\n"
  echo -e "\t\t - verbosity flag -v N where N=1..4 optional;\n\t\t - include before or after tag flags\n"
}

TAGSTRING=""

while (( "$#" )); do

        case $1 in
          -t | --tags )
            TAGSTRING="--tags $2 "
            shift 2
            ;;
          -s | --skip-tags )
            TAGSTRING="--skip-tags $2 "
            shift 2
            ;;
          -v | --version )
            if ! [[ "$2" =~ ^[0-9]+$ ]]
            then
                    echo "ERROR: -v is not an integer"
                    exit 1
            elif [ "$2" -ge 1 ] && [ "$2" -le 4 ]
            then
                    vs=`printf '%*s' "$2" | tr ' ' "v"`
                    TAGSTRING="-$vs "
                    shift 2
            else
                    echo "ERROR: -v value $2 is not in range [1..4]"
                    exit 1
            fi
            ;;
          "" )
          ;;
          * )
            usage
            exit 1
        esac

done

# ensure correct version of ansible
if ansible --version | grep --quiet -E 'ansible 2.2.|ansible 2.1.|ansible 2.3.|ansible 2.4.|ansible 2.5.|ansible 2.6.'
then
  echo "$PFX Ansible found, acquiring GalaxyKickStart.."



  if [ ! -d "./roles/galaxy.movedata" ]; then

    # acquire GKS
      # this requires a somewhat newer version of git (2.11+)
    git clone $SHALLOW https://github.com/ARTbio/GalaxyKickStart.git temporino
    cd temporino || exit
    git reset --hard $GKS_SHA_PIN

    # append line to ansible.cfg to force paramiko if sshpass absent
    if sshpass -V 1>/dev/null 2>&1
    then
      TRANSPORT_CFG_LINE="transport = ssh"
    else
      printf "${RED}WARNING!{$NC} Paramiko transport selected. If there are errors / port conflicts while running script (particularly when resetting proftpd in the galaxy.movedata role), consider installing sshpass so that ansible can use ssh transport."
    fi
    echo $TRANSPORT_CFG_LINE >> ansible.cfg
    cd .. || exit
    rm -f temporino/galaxy.yml
    rm -f temporino/.git
    
    # acquire workflows
    mkdir -p gonramp/workflows
    git clone $WORKFLOWS --depth 1 gonramp/workflows
    rm -rf gonramp/workflows/LICENSE

    cp -R ./temporino/ .
    rm -rf temporino

    mv gonramp_vars group_vars/gonramp

    ansible-galaxy install -r requirements_roles.yml -p roles
    # acquire apollo role
    # git clone https://github.com/goeckslab/ansible-apollo.git roles/apollo
    # copy over modifications to existent roles
    cp -Rf modified_roles/* roles/

  else
    echo "$PFX previous GalaxyKickStart installation found, resuming"
  fi

  export ANSIBLE_HOST_KEY_CHECKING=False

  # install galaxy,
  echo "$PFX Installing G-OnRamp ... "
  printf "${RED}WARNING!${NC} This will take some time (upwards of an hour)\n"
  ansible-playbook -i ./gonramp_inventory gonramp.yml $TAGSTRING
  R=$?

  if [[ $R -eq 0 ]]
  then
    echo "$PFX G-OnRamp installation successful!"
  else
    echo "G-OnRamp Installation failure"
  fi
else
  echo "$PFX ERROR: NO ANSIBLE FOUND WITH CORRECT VERSION ( >= 2.1)"
fi

if (( $SECONDS > 3600 )) ; then
  let "hours=SECONDS/3600"
  let "minutes=(SECONDS%3600)/60"
  let "seconds=(SECONDS%3600)%60"
  echo "Completed in $hours hour(s), $minutes minute(s) and $seconds second(s)"
elif (( $SECONDS > 60 )) ; then
  let "minutes=(SECONDS%3600)/60"
  let "seconds=(SECONDS%3600)%60"
  echo "Completed in $minutes minute(s) and $seconds second(s)"
else
  echo "Completed in $SECONDS seconds"
fi
