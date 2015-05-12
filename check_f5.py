#!/usr/bin/env python
import bigsuds
import argparse
import sys

# Basic stuff. Get the args from nag or user
parser = argparse.ArgumentParser(description='Gimme your host detes')
parser.add_argument('-o', "--host",
                    action='store', dest='host',
                    help='The hostname or IP address of the F5 LB')
parser.add_argument('-u', '--user',
                    action='store', dest='user',
                    help='Username with API access')
parser.add_argument('-p', '--password',
                    action='store', dest='password',
                    help='A plaintext password')
parser.add_argument('-P', '--pool',
                    action='store', dest='pool_name',
                    help ='F5 Traffic Pool name')
parser.add_argument('-V', '--vserver',
                    action='store', dest='vs_name',
                    help ='F5 Virtual Server name')

# Parse args and store them for later 
opts = parser.parse_args()
host = opts.host
user = opts.user
password = opts.password
vs_name = opts.vs_name
pool_name = opts.pool_name

# Instantiate the API session
b = bigsuds.BIGIP(hostname = host, username=user, password=password, debug=True)

# Use iControl API to query the status of a vs
def get_vs_status(vs_name):
    try:
        status_list = b.LocalLB.VirtualServer.get_object_status([vs_name])
        status_desc =  status_list[0]['status_description']
        status_avail = status_list[0]['availability_status']
    except:
       print "UKNOWN - Unable to find vserver %s" % vs_name
       sys.exit(3)
    if status_avail == 'AVAILABILITY_STATUS_RED':
         print "CRITICAL - %s: %s" % (vs_name, status_desc)
         sys.exit(2)
    elif status_avail == 'AVAILABILITY_STATUS_GREEN':
        print "OK - %s: %s" % (vs_name, status_desc)
        sys.exit(0)
    else:
        print "UKNOWN - %s: query returned \"%s\"" % (vs_name, status_desc)
        sys.exit(3)

# Do basically the same thing for pool status
def get_pool_status(pool_name):
    try:
        status_list = b.LocalLB.Pool.get_object_status([pool_name])
        status_desc =  status_list[0]['status_description']
        status_avail = status_list[0]['availability_status']
    except:
       print "UKNOWN - Unable to find pool %s" % pool_name
       sys.exit(3)
    if status_avail == 'AVAILABILITY_STATUS_RED':
         print "CRITICAL - %s: %s" % (pool_name, status_desc)
         sys.exit(2)
    elif status_avail == 'AVAILABILITY_STATUS_GREEN':
        print "OK - %s: %s" % (pool_name, status_desc)
        sys.exit(0)
    else:
        print "UKNOWN - %s: query returned \"%s\"" % (pool_name, status_desc)
        sys.exit(3)

# Main function. Basic logic so we pick which item to monitor
if __name__ == "__main__":
    if vs_name:
        get_vs_status(vs_name)
    elif pool_name:
        get_pool_status(pool_name)
    else:
        print "No object given"
        sys.exit()
