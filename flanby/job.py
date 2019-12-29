from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import nmap
import logging

# Get an instance of a logger
logger = logging.getLogger("flanby")

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", minutes=20)
def full_scan():
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts='192.168.1.1-254', ports='21-443')

    # run a loop to print all the found result about the ports
    for host in nmScan.all_hosts():
        logger.debug('Host : %s (%s)' % (host, nmScan[host].hostname()))
        logger.debug('State : %s' % nmScan[host].state())
        # for proto in nmScan[host].all_protocols():
        #     logger.debug('| Protocol : %s' % proto)
        #
        #     lport = nmScan[host][proto].keys()
        #     # lport.sort()
        #     for port in lport:
        #         logger.debug('-->port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
    logger.debug("full_scan jod done")


def callback_result(host, scan_result):
    message = host + "-> " + scan_result
    logger.debug(message)


@register_job(scheduler, "interval", minutes=20)
def async_scan():
    nmScan = nmap.PortScannerAsync()
    nmScan.scan(hosts='192.168.1.1-254', ports='21-443', callback=callback_result)
    while nmScan.still_scanning():
        pass
        # logger.debug("Waiting ...")

    # for host in nmScan.all_hosts():
    #     logger.debug('Host : %s (%s)' % (host, nmScan[host].hostname()))
    #     logger.debug('State : %s' % nmScan[host].state())
    #     for proto in nmScan[host].all_protocols():
    #         logger.debug('| Protocol : %s' % proto)
    #
    #         lport = nmScan[host][proto].keys()
    #         # lport.sort()
    #         for port in lport:
    #             logger.debug('-->port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
    logger.debug("async_scan jod done")

register_events(scheduler)

scheduler.start()
logger.debug("Scheduler started!")
