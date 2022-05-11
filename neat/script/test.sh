#!/usr/bin/env bash

function main(){
	config=${0%\.*}.conf
  source $config
  echo $mysql_ip
}
main