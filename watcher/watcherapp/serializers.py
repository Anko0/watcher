from rest_framework import serializers

from .models import Metrix


class MetrixSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metrix
        fields = ['metrix_token', 'metrix_created', 'metrix_cpu', 'metrix_ram', 
                  'metrix_swap', 'metrix_rom', 'metrix_proc', 'metrix_netconn', 
                  'metrix_netif', 'metrix_uname', 'metrix_users']      