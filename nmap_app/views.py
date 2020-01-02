from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from .models import Server, Port
from nmap_app.job import *

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger("flanby")


def index(request):
    # TODO: integrate paginated table
    latest_server_list = Server.objects.order_by('-creation_date')
    context = {'latest_server_list': latest_server_list}
    logger.debug("list servers")
    return render(request, 'nmap/index.html', context)


def detail(request, server_ip):
    # TODO: a better code with cleaning input to avoid sql injection
    #scan_job()
    logger.debug("list ports from server {}".format(server_ip))
    try:
        servers = Server.objects.filter(server_ip=server_ip)

    except Server.DoesNotExist:
        raise Http404("Server does not exist")

    try:
        ports = Port.objects.filter(server_id=servers.all()[0])
    except Port.DoesNotExist:
        raise Http404("Port does not exist")
    return render(request, 'nmap/detail.html', {'servers': servers, 'ports': ports})