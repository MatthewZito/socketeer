#!/usr/bin/env bash
#filename       :pre_task.sh
#desc           :update local history and checkout provided commit via shasum
#author         :Matthew Zito (goldmund)
#created        :03/2021
#version        :1.0.0
#usage          :n/a - automated invocation
#environment    :bash 5.0.17
#===============================================================================


IFS=$'\n'

main() {
  local repository_dir=$1
  local commit_sha=$2

  if [[ $UID -eq $ROOT_UID ]]; then
    panic $E_NOROOT "Cannot execute as root"
  fi

  pushd $repository_dir &>/dev/null
  [[ $? -ne 0 ]] && panic $E_FILENOTFOUND "Repository not found at $repository_dir"

  git clean -d -f -x 2>/dev/null
  [[ $? -ne 0 ]] && panic $E_GIT "Failed to clean repository"

  git pull
  [[ $? -ne 0 ]] && panic $E_GIT "Failed to pull repository history"

  git reset --hard "$commit_sha"
  [[ $? -ne 0 ]] && panic $E_GIT "Failed to checkout given commit SHA"

}

# local constants
ROOT_UID=0

E_NOROOT=87
E_FILENOTFOUND=2
E_ARGS=88
E_GIT=89

UTIL_FILE='utils.sh'
EXE_LOC=$(dirname "$0")

source $EXE_LOC/$UTIL_FILE

set -o errexit
set -o nounset

main $*