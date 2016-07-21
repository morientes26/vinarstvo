#!/usr/bin/env bash

# Functions ==============================================

# source: https://gist.github.com/JamieMason/4761049
function program_is_installed {
  local return_=1
  type $1 >/dev/null 2>&1 || { local return_=0; }
  echo "$return_"
}

function npm_package_is_installed {
  local return_=1
  ls node_modules | grep $1 >/dev/null 2>&1 || { local return_=0; }
  echo "$return_"
}

function directory_exists {
    local return_=0
    if [ -d "$1" ]; then
        local return_=1
    fi
    echo "$return_"
}

function echo_fail {
  printf "\e[31m✘ ${1}"
  #echo "\033[0m"
}

function echo_pass {
  printf "\e[32m✔ ${1}"
  #echo "\033[0m"
}

function echo_if {
  if [ $1 == 1 ]; then
    echo_pass $2
  else
    echo_fail $2
  fi
}

function install_if_not_installed {
  if [ $1 == 1 ]; then
    echo_pass " ${2} \n"
  else
    echo_fail " ${2} \n"

    if [ $2 == "nodejs" ]; then
        sudo apt-get install nodejs
    fi

    if [ $2 == "npm" ]; then
        sudo apt-get install npm
    fi

    if [ $2 == "bower" ]; then
        sudo npm install bower -g
    fi

    if [ $2 == "bower_components" ]; then
        echo "bower install"
        #bower install
    fi

  fi
}

# ============================================== Functions

# command line programs
#echo "node          $(echo_if $(program_is_installed node))"

install_if_not_installed $(program_is_installed nodejs) nodejs
install_if_not_installed $(program_is_installed npm) npm
install_if_not_installed $(program_is_installed bower) bower
install_if_not_installed $(directory_exists bower_components) bower_install




