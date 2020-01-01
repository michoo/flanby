import datetime
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from flanby.settings import FLANBY_NETWORK_SCAN_JOB, FLANBY_TIME_SCAN_JOB
from .models import Server, Port

import logging
import nmap

nmScan = nmap.PortScanner()

# Get an instance of a logger
logger = logging.getLogger("flanby")

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", minutes=FLANBY_TIME_SCAN_JOB)
def scan_job():
    logger.debug("I'm a test job!")
    latest_server_list = Server.objects.all()
    # logger.debug(latest_server_list[0])

    nmScan = nmap.PortScanner()
    nmScan.scan(hosts=FLANBY_NETWORK_SCAN_JOB)
    logger.debug(nmScan)

    for host in nmScan.all_hosts():
        logger.debug(host)
        server_id =1
        if nmScan[host].state() == 'up':
            value_status = True
        else:
            value_status = False
        try:
            obj = Server.objects.get(server_ip=host)
            obj.status_up = value_status
            obj.last_update = timezone.now()
            obj.save()
            server_id = obj.pk
        except Server.DoesNotExist:
            date_to_save = timezone.now()
            obj = Server.objects.create(server_ip=host, status_up=value_status,
                                        creation_date=date_to_save, last_update=date_to_save)
            server_id = obj.pk
        try:
            ports_obj = Port.objects.filter(server_id=server_id).values_list('port_number', flat=True)
        except Port.DoesNotExist:
            exit()

        for proto in nmScan[host].all_protocols():
            logger.debug('| Protocol : %s' % proto)

            lport = nmScan[host][proto].keys()
            # lport.sort()
            for port in lport:
                logger.debug('-->port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
                if port in ports_obj:
                    try:
                        port_obj = Port.objects.filter(port_number=port, server_id=server_id)
                        port_obj.last_update=timezone.now()
                        port_obj.status = nmScan[host][proto][port]['state']
                        port_obj.save()
                    except Port.DoesNotExist:
                        pass

                else:
                    date_to_save = timezone.now()
                    comment = "product: {}, extrainfo: {}, reason: {}, version: {}, conf: {}, cpe: {}".format(
                        nmScan[host][proto][port]['product'],
                        nmScan[host][proto][port]['extrainfo'],
                        nmScan[host][proto][port]['reason'],
                        nmScan[host][proto][port]['version'],
                        nmScan[host][proto][port]['conf'],
                        nmScan[host][proto][port]['cpe'])
                    port_obj = Port.objects.create(port_name=nmScan[host][proto][port]['name'], protocol=proto,
                                                   port_number=port, comment=comment,
                                                   status= nmScan[host][proto][port]['state'],
                                                   creation_date=date_to_save, last_update=date_to_save,
                                                   server_id=server_id)

    logger.debug("scan job done")


register_events(scheduler)

scheduler.start()
logger.debug("Scheduler started!")
