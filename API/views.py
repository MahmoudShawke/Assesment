from .serlizer import *

import jwt, datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
import time



# Create your views here.
class CHECK:
    def get( self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            # raise AuthenticationFailed('Unauthenticated!')
            return HttpResponseRedirect('/employee/login')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Employee.objects.filter(id=payload['id']).first()
        serializer = empSerializer(user)

        return user


@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        contex = 'Unauthenticated'
        return Response(contex)

    else:

        user = empSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data)
        return Response(user.errors)


@api_view(['POST', 'GET'])
def get_user(request):
    token = request.COOKIES.get('jwt')

    if not token:
        contex = 'Unauthenticated'
        return Response(contex)

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        contex = 'Unauthenticated'
        return Response(contex)

    user = Employee.objects.filter(id=payload['id']).first()
    serializer = empSerializer(user)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def Login(request):
    if request.method == 'GET':
        token = request.COOKIES.get('jwt')
        if token:
            return Response(token)
        else:
            contex = 'Unauthenticated'
            return Response(contex)
    else:
        email = request.data['email']
        password = request.data['password']
        user = Employee.objects.filter(email=email).first()
        if user is None:
            contex = 'User not found!'
            return Response(contex)

        if user.password != password:
            contex = 'Incorrect password!'
            return Response(contex)
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
    return response


@api_view(['GET', 'POST'])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    return response


@api_view(['GET'])
def attendence(request):
    x = CHECK()
    user = x.get(request)
    try:
        x = user.first_name
        context = {}
        context['user'] = user
        context['attend'] = Attendance.objects.filter(user_id=user.id)
        x = Attendance.objects.filter(user_id=user.id)
        serializer = attendSerializer(x, many=True)

        return Response(serializer.data)
    except:
        contex = 'Unauthenticated'
        return Response(contex)


@api_view(['POST'])
def att_record(request):
    x = CHECK()
    user = x.get(request)
    try:
        x = user.first_name
        IP_addres = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        if user.IPAddress == IP_addres:
            if bool(Attendance.objects.filter(user=user.id, date=datetime.date.today())):

                contex = 'ALready Submited Attendance  Today'
                return Response(contex)
            else:
                user = attendreSerializer(data=request.data)
                if user.is_valid():
                    user.save()
                    return Response(user.data)
                return Response(user.errors)

        else:
            contex = ' could not submit Attendance With This Device'
            return Response(contex)
    except:
        contex = 'Unauthenticated'
        return Response(contex)

@api_view(['GET'])
def check(request):
    x = CHECK()
    user = x.get(request)
    try:
        x = user.first_name
        context = {}
        context['user'] = user
        x = Attendance.objects.filter(user_id=user.id).first()
        x = Checks.objects.filter(Check=x)
        context['check'] = x
        serializer = checkSerializer(x, many=True)

        return Response(serializer.data)
    except:
        contex = 'Unauthenticated'
        return Response(contex)


@api_view(['POST'])
def checkio(request, list_id):
    x = CHECK()
    user = x.get(request)
    try:
        x = user.first_name
        IP_addres = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        if user.IPAddress == IP_addres:
            if bool(Attendance.objects.filter(user=user.id, date=datetime.date.today())):
                newemp = Attendance.objects.filter(id=list_id).first()
                if newemp.checkFI == 'OU':
                    request.data['description'] = 'CHECK IN'
                    serializer = checkSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        newemp.checkin = int(newemp.checkin) + 1
                        newemp.checkFI = 'IN'
                        newemp.save()
                        return Response(serializer.data)
                elif newemp.checkFI == 'IN':
                    request.data['description']='CHECK OUT'
                    serializer = checkSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        newemp.checkout = int(newemp.checkout) + 1
                        newemp.checkFI = 'OU'
                        newemp.save()
                        return Response(serializer.data)
                else:
                    request.data['description'] = 'CHECK IN'
                    serializer = checkSerializer(data=request.data)
                    if serializer.is_valid():

                        serializer.save()
                        newemp = Attendance.objects.filter(id=list_id).first()
                        newemp.checkin = int(newemp.checkin) + 1
                        newemp.checkFI = 'IN'
                        newemp.save()
                        return Response(serializer.data)
            else:


                return HttpResponseRedirect("/employee/login")
        else:
            print('U Couldnot  Submit Attendance With This Device')
    except:
        contex = 'Unauthenticated'
        return Response(contex)