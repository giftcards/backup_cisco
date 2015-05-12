## Synopsis

Simple script to log into cisco switches and download running and vlan configurations as well as a snapshot of the interface status.

## Example

This script is intended to be run once a day as a cronjob. It uses paramiko to login to a list of switches and backup the contents of the following commands.

show running-config
show vlan
show int status

## Motivation

This was written in the process of rebuilding a small network.

## Installation

Script should be setup to run once a day, tested working on CentOS 6.
Requires python > 2.6 and paramiko pip module.
Requires a user to login to the switch via SSH and an enable password.
Requires access to the commands listed in the Example section.
backup_cisco.conf needs copied to /etc/ and updated for your environment.

## Contributors

Ryan Munz for Giftcards.com - May 2015
