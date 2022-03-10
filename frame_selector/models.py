from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser    # アカウント認証関連



class Memo(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Frame(models.Model):
    # Id = 自動採番かも？
    frame_code  = models.CharField(max_length=150) # フレーム判定用コード　記載必須に変更が必要
    maker = models.CharField(max_length=150)
    model_name = models.CharField(max_length=150)
    size = models.CharField(max_length=150)
    model_year = models.CharField(max_length=150)
    maker_url = models.CharField(max_length=150)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.frame_code

    
class Input_values(models.Model):
    frame_code       = models.CharField   (default='USER_INPUT_VALUES', max_length=150) # フレーム判定用コード　記載必須に変更が必要
    seat_tube        = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,)   # A:SEAT TUBE
    seat_angle       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # B:SEAT ANGLE
    top_tube         = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # C:TOP TUBE
    head_tube        = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # D:HEAD TUBE
    head_angle       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # E:HEAD ANGLE
    wheel_base       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # F:WHEEL BASE
    rear_senter      = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # G:REAR CENTER
    bb_drop          = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # H:BB DROP
    stack            = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # I:STACK
    reach            = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # J:REACH
    maker_url        = models.CharField(max_length=200, null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.frame_code
    
    
class Account(models.Model):
    account_name = models.CharField(max_length=150)
    password  = models.CharField(max_length=150)
    seat_tube        = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,)   # A:SEAT TUBE
    seat_angle       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # B:SEAT ANGLE
    top_tube         = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # C:TOP TUBE
    head_tube        = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # D:HEAD TUBE
    head_angle       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # E:HEAD ANGLE
    wheel_base       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # F:WHEEL BASE
    rear_senter      = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # G:REAR CENTER
    bb_drop          = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # H:BB DROP
    stack            = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # I:STACK
    reach            = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)   # J:REACH
    last_login_time  = models.DateTimeField(blank=True, null=True)  # 最終ログインがかなり前のアカウントは削除するため
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
        

    def __str__(self):
        return self.account_name
    
    