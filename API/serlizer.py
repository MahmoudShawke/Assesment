from rest_framework import routers, serializers, viewsets

from .models import *

class empSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields ='__all__'

class attendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields =('__all__')

    # user = empSerializer(many=False)

class attendreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields =('id','description','user')

class checkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields ='__all__'