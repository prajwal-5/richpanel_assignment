from django.db import models
class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=150)
    # plan_type = models.OneToOneField(Plan, on_delete = models.CASCADE, null=True, blank=True)
    plan_period = models.IntegerField(null=True, blank=True, default=1)
    is_loggedin = models.BooleanField(default=False)

    
    def __int__(self):
        return self.name

    def duration(self):
        return self.plan_period

    def is_authenticated(self):
        return self.is_loggedin



# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=150)
    monthly_price = models.IntegerField()
    yearly_price = models.IntegerField()
    video_quality = models.CharField(max_length=100)
    resolution = models.CharField(max_length=150)
    devices = models.CharField(max_length=100)
    active_screens = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def m_price(self):
        return self.monthly_price

    def a_price(self):
        return self.yearly_price

    def device_list(self):
        return self.devices.split('+')
