from poolproject.pool.models import Pool, CustomUser, Booking
from rest_framework import serializers

class PoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pool
        fields = '__all__'
