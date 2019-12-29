#!/usr/bin/env python


import logging
import masscan
import logging.config

import yaml

# logging settings
with open('./logging.yml', 'rt') as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)

# Get an instance of a logger
logger = logging.getLogger("flanby")

mas = masscan.PortScanner()
mas.scan('192.168.1.1/24', arguments='--max-rate 1000000')
logger.debug(mas.scan_result)

logger.debug("masscan job done")
