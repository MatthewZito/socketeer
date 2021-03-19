#!/usr/bin/env bash

IFS=$'\n'

current_time() {
  echo $(date +'%Y-%m-%dT%H:%M:%S%z')
}

panic() {
  local exit_status=$1

  shift # pop exit status; we don't want to print it

  echo "[-] ERROR ($(current_time)): $*" >&2
  exit $exit_status
}
