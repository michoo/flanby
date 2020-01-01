from django.contrib import admin

# Register your models here.
from .models import Server, Port

class PortAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'port_name', 'port_number', 'server_id']

    # define search columns list, then a search box will be added at the top of Department list page.
    search_fields = ['port_name', 'port_number']

    # define filter columns list, then a filter widget will be shown at right side of Department list page.
    list_filter = ['port_name', 'port_number']

    # define which field will be pre populated.
    prepopulated_fields = {'port_name': ('port_name',)}

    # define model data list ordering.
    ordering = ('id', 'port_name')

class ServerAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'server_ip', 'status_up']

    # define search columns list, then a search box will be added at the top of Department list page.
    search_fields = ['server_ip', 'status_up']

    # define filter columns list, then a filter widget will be shown at right side of Department list page.
    list_filter = ['server_ip', 'status_up']

    # define which field will be pre populated.
    prepopulated_fields = {'server_ip': ('server_ip',)}

    # define model data list ordering.
    ordering = ('id', 'server_ip')

admin.site.register(Server, ServerAdmin)
admin.site.register(Port, PortAdmin)