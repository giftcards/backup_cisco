#!/usr/bin/python
import paramiko
import ConfigParser
import datetime
from time import sleep

# Datestring can be overridden to run jsons for a specific date
datestring = str(datetime.date.today())

# Read our config file
config = ConfigParser.RawConfigParser()
config.read('/etc/backup_cisco.conf')

username = config.get('credentials', 'username')
#print "username : %s" % username
password = config.get('credentials', 'password')
#print "password : %s" % password
enable = config.get('credentials', 'enable')
#print "enable : %s" % enable

for key, switch in config.items('switches') :

    print "Open Connection : %s" % switch
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(switch, username=username, password=password, look_for_keys=False, allow_agent=False)

    print "Invoke Shell : %s" % switch
    remote_conn = remote_conn_pre.invoke_shell()
    remote_conn.send("terminal length 0\n")

    print "Enter Privileged Mode : %s" % switch
    remote_conn.send("en\n")
    sleep(1)
    remote_conn.send(enable+'\n')
    sleep(1)
    remote_conn.recv(1000)

    print "show running-config : %s" % switch
    remote_conn.send("show running-config\n")
    sleep(5)
    running_config = remote_conn.recv(100000)

    print "show vlan : %s" % switch
    remote_conn.send("show vlan\n")
    sleep(5)
    vlan = remote_conn.recv(100000)

    print "show int status : %s" % switch
    remote_conn.send("show int status\n")
    sleep(5)
    int_status = remote_conn.recv(100000)

    print "Shutdown Connection : %s" % switch
    remote_conn.send("exit\n")
    del(remote_conn)
    del(remote_conn_pre)

    running_config_file = config.get('backups', 'backupdir')+'/'+switch+'-running_config-'+datestring+'.cisco'
    print "writing running_config_file : %s" % running_config_file
    f = open(running_config_file, 'w')
    f.write(running_config)
    f.close

    vlan_file = config.get('backups', 'backupdir')+'/'+switch+'-vlan-'+datestring+'.cisco'
    print "writing vlan_file : %s" % vlan_file
    f = open(vlan_file, 'w')
    f.write(vlan)
    f.close

    int_status_file = config.get('backups', 'backupdir')+'/'+switch+'-int_status-'+datestring+'.cisco'
    print "writing int_status_file : %s" % int_status_file
    f = open(int_status_file, 'w')
    f.write(int_status)
    f.close
