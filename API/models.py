from django.db import models
from computed_property import ComputedCharField,ComputedDateField,ComputedTimeField
import time
import jwt, datetime,socket,re,uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Employee(AbstractUser):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=50)
    IPAddress = ComputedCharField(max_length=3 * 64, compute_from='ip',null=True)
    Hostnametest = ComputedCharField(max_length=3 * 64, compute_from='host',null=True)
    username = None
    user_name = ComputedCharField(max_length=3 * 64, compute_from='user',unique=True,null=True)


    @property
    def host(self):
        h_name = socket.gethostname()
        return h_name

    @property
    def ip(self):
        IP_addres = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return IP_addres


    @property
    def user(self):

        return self.first_name+''+self.last_name

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "user_name"

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=True)
    date = ComputedDateField(editable=False,null=True,compute_from='datee')
    time = ComputedTimeField(editable=False,null=True,compute_from='timee')
    checkin=models.CharField(max_length=3,null=True,default=0)
    checkout=models.CharField(max_length=3,null=True,default=0)

    checks = [
        ('IN', 'CheckIN'),
        ('OU', 'CheckOUT'),


    ]
    checkFI = models.CharField(
        max_length=2,
        choices=checks,default=''
    )
    @property
    def datee(self):
        date=datetime.date.today()
        return date

    @property
    def timee(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time



class Checks(models.Model):
    id = models.AutoField(primary_key=True)
    Check = models.ForeignKey(Attendance, on_delete=models.CASCADE,related_name='Check_attendances')
    description = models.CharField(max_length=100, null=True)
    date = ComputedDateField(editable=False,null=True,compute_from='datee')
    time = ComputedTimeField(editable=False,null=True,compute_from='timee')

    @property
    def datee(self):
        date=datetime.date.today()
        return date

    @property
    def timee(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time






