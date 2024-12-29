import rest_framework.status
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse

from .models import Pool, CustomUser, Booking
from .serializers import PoolSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ChangePoolStatus(APIView):
    def post(self, request, pool_id):
        curUser = CustomUser.objects.get(
            login=request.data.get('login'), password=request.data.get('login')
            )
        if (curUser):
            if curUser.role == 'Admin':
                pool = Pool.objects.get(pool_id=pool_id)
                if (pool):
                    if pool.status == "Opened":
                        pool.status = "Closed"
                    else:
                        pool.status = "Opened"
                    return Response(status=rest_framework.status.HTTP_200_OK)
                else:
                    return Response(status=rest_framework.status.HTTP_404_NOT_FOUND,
                                     data={'reason': 'No such pool found'})
            else:
                 return Response(status=rest_framework.status.HTTP_403_FORBIDDEN,
                                 data={'reason': 'You have no permission to do that'})
        else:
            return Response(status=rest_framework.status.HTTP_404_NOT_FOUND,
                    data={'reason': 'No such user found'})

class GetPoolsList(APIView):
    def get(self, request):
        state_param = self.request.query_params.get('state', None)
        capacity_param = self.request.query_params.get('capacity', None)
        pools = Pool.objects.all()
        if state_param:
            if state_param == "Opened":
                pools = pools.filter(status="Opened")
            elif state_param == "Closed":
                pools = pools.filter(status='Closed')
        if capacity_param:
            if capacity_param == "Full":
                pools = pools.filter(current_capacity__gt=0)
            elif capacity_param == "NotFull":
                pools = pools.filter(current_capacity=0)
        return JsonResponse(status=rest_framework.status.HTTP_200_OK, data=PoolSerializer(pools).data)


class OrderPool(APIView):
    def post(self, request, pool_id):
        curUser = CustomUser.objects.get(
            login=request.data.get('login'), password=request.data.get('password')
            )
        if (curUser):
            pool = Pool.objects.get(pool_id=pool_id)
            if (pool):
                if (pool.capacity_left > 0):
                    booking_line = Booking.objects.get(user=curUser.id, pool=pool_id)
                    if (booking_line):
                        return Response(status=rest_framework.status.HTTP_400_BAD_REQUEST,
                                        data={'reason': 'You cannot book twice'})
                    else:
                        pool.capacity_left -=1
                        Booking.objects.create(user=curUser.id, pool=pool_id)
                        return Response(status=rest_framework.status.HTTP_200_OK)
                return Response(status=rest_framework.status.HTTP_400_BAD_REQUEST,
                                data={'reason': 'No space left'})
            else:
                return Response(status=rest_framework.status.HTTP_404_NOT_FOUND,
                                data={'reason': 'No such pool found'})
        else:
            return Response(status=rest_framework.status.HTTP_404_NOT_FOUND,
                            data={'reason': 'No such user found'})
