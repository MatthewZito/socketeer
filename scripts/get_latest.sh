#!/usr/bin/env bash
#filename       :update_repo.sh
#desc           :update local history and persist latest commit id, if changed
#author         :Matthew Zito (goldmund)
#created        :03/2021
#version        :1.0.0
#usage          :n/a
#environment    :bash 5.0.17
#===============================================================================

main() {
  local repo=$1

  if [[ $UID -eq $ROOT_UID ]]; then
    panic $E_NOROOT "Cannot execute as root"
  fi

  if [[ -e "$LATEST_COMMIT_FILE" ]]; then
    rm -f "$LATEST_COMMIT_FILE"
  fi

  hard_reset $repo

  commit_id=$(get_latest)

  # update and get latest; eval SHA diff
  git pull
  [[ $? -ne 0 ]] && panic $E_GIT "Failed to pull latest"

  new_commit_id=$(get_latest)

  # if we've a newer commit, persist it
  if [ $new_commit_id != $commit_id ]; then
    popd 1> /dev/null
    echo $new_commit_id > "$LATEST_COMMIT_FILE"
  fi

}

# local constants
ROOT_UID=0

E_NOROOT=87
E_FILENOTFOUND=2
E_ARGS=88
E_GIT=89

LATEST_COMMIT_FILE='.commit_id'
UTIL_FILE='utils.sh'
EXE_LOC=$(dirname "$0")

source $EXE_LOC/$UTIL_FILE

# nav to repository, reset to HEAD
hard_reset() {
  local repository_dir=$1

  pushd $repository_dir &>/dev/null
  [[ $? -ne 0 ]] && panic $E_FILENOTFOUND "Repository not found at $repository_dir"

  git reset --hard HEAD &>/dev/null
  [[ $? -ne 0 ]] && panic $E_GIT "Failed to reset state to HEAD"

  return 0
}

# fetch most recent commit SHA
get_latest() {
  latest_commit=$(git log -n1 --format=format:%H)

  [[ $? -ne 0 ]] && panic $E_GIT "Failed to log Git history"

  echo $latest_commit
}

set -o errexit
set -o nounset

main $1
