from django.db import models

class status(models.Model):
    ToDo = models.FloatField(null=True)
    Done = models.FloatField(null=True)
    Contrag = models.CharField(max_length=1000, null=True)
    Amount_Cars = models.CharField(max_length=10, null=True)
    Num_Cars = models.CharField(max_length=2000, null=True)
    Time = models.DateTimeField(null=True)


class status(models.Model):
    ToDo = models.FloatField(null=True)
    Done = models.FloatField(null=True)
    Contrag = models.CharField(max_length=1000, null=True)
    Amount_Cars = models.CharField(max_length=10, null=True)
    Num_Cars = models.CharField(max_length=2000, null=True)
    Time = models.DateTimeField(null=True)


class weights(models.Model):
    Time = models.DateTimeField(null=True)
    Material = models.CharField(max_length=100, null=True)
    Mass = models.FloatField(null=True)
    Contrag = models.CharField(max_length=100, null=True)
    Car_Num = models.CharField(max_length=20, null=True)
    PBA = models.CharField(max_length=20, null=True)

class income(models.Model):
    Time = models.DateTimeField(null=True)
    Material = models.CharField(max_length=100, null=True)
    Mass = models.FloatField(null=True)
    Contrag = models.CharField(max_length=100, null=True)
    Stock = models.CharField(max_length=5, null=True)

class driver(models.Model):
    chat = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, null=True)
    uid = models.IntegerField(null=True)
    car_num = models.CharField(max_length=20, null=True)
    car_num_short = models.IntegerField(null=True)
    tsm = models.CharField(max_length=5, null=True)
    car_num = models.CharField(max_length=100, null=True)    
    car_num_short = models.CharField(max_length=50, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    vel = models.FloatField(null=True)
    lat_old = models.FloatField(null=True)
    lng_old = models.FloatField(null=True)
    zone = models.CharField(max_length=200, null=True)
    in_zoneList = models.IntegerField(null=True)
    # airport_msg_time = models.DateTimeField(null=True)
    airport_msg_time = models.CharField(max_length=200, null=True)
    airport_msg = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.car_num


class coor(models.Model):
    chat = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, null=True)
    uid = models.IntegerField(null=True)
    car_num = models.CharField(max_length=20, null=True)
    car_num_short = models.IntegerField(null=True)
    tsm = models.CharField(max_length=5, null=True)
    car_driver = models.CharField(max_length=50, null=True)
    car_driver_short = models.CharField(max_length=100, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    vel = models.FloatField(null=True)
    lat_old = models.FloatField(null=True)
    lng_old = models.FloatField(null=True)
    zone = models.CharField(max_length=200, null=True)
    in_zoneList = models.IntegerField(null=True)
    # airport_msg_time = models.DateTimeField(null=True)
    airport_msg = models.CharField(max_length=200, null=True)
    airport_msg_time = models.CharField(max_length=200, null=True)
    tg_id = models.IntegerField(null=True)
    y_url = models.CharField(max_length=300, null=True)
    y_min = models.FloatField(null=True)
    y_km = models.FloatField(null=True)
    task_full_name = models.CharField(max_length=300, null=True)
    task_full_coor = models.CharField(max_length=300, null=True)
    task_left_name = models.CharField(max_length=100, null=True)
    task_right_name = models.CharField(max_length=300, null=True)
    task_left_coor = models.CharField(max_length=100, null=True)
    task_right_coor = models.CharField(max_length=300, null=True)
    isTask = models.IntegerField(null=True)
    task_amount = models.IntegerField(null=True)
    task_cur = models.IntegerField(null=True)
    rope_ZoneCoorList = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.car_num


