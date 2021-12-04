from rest_framework import serializers

from .models import Active, Metrix


class ActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Active
        fields = ['active_name', 'active_token', 'active_hostname', 'active_ip', 
                  'active_description', 'active_created']


class MetrixSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metrix
        fields = ['metrix_token', 'metrix_created', 'metrix_cpu', 'metrix_ram', 
                  'metrix_swap', 'metrix_rom', 'metrix_proc', 'metrix_netconn', 
                  'metrix_netif', 'metrix_uname', 'metrix_users']
        