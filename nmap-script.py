#!/usr/bin/env python

import nmap
import logging
import os

import logging.config

import yaml

# logging settings
with open('./logging.yml', 'rt') as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)

# Get an instance of a logger
logger = logging.getLogger("flanby")


nmScan = nmap.PortScanner()
location = os.getcwd()
final_location = location + '/scripts/vulners.nse'

final_arg = '-sV --script='+final_location
logger.debug(final_arg)
nmScan.scan(hosts='192.168.1.1', arguments=final_arg)
logger.debug(nmScan.command_line())


for host in nmScan.all_hosts():
    logger.debug('Host : %s (%s)' % (host, nmScan[host].hostname()))
    logger.debug('|State : %s' % nmScan[host].state())
    for proto in nmScan[host].all_protocols():
        logger.debug('| Protocol : %s' % proto)

        lport = nmScan[host][proto].keys()
        # lport.sort()
        for port in lport:
            logger.debug('|-->port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
logger.debug("async_scan job done")



