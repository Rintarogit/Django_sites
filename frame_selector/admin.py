from django.contrib import admin

# Register your models here.
from .models import Memo
from .models import Input_values
from .models import Frame
from .models import Account
# adminサイトのCSV管理機能
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class MemoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_datetime', 'updated_datetime')
    list_display_links = ('id', 'title')

admin.site.register(Memo, MemoAdmin)


# class Input_valuesAdmin(admin.ModelAdmin):
#     list_display = ('frame_code','seat_tube', 'seat_angle', 'top_tube', 'head_tube', 'head_angle', 'wheel_base', 'rear_senter', 'bb_drop','stack', 'reach')
#     list_display_links = ('seat_tube', 'seat_angle')

# admin.site.register(Input_values, Input_valuesAdmin)


# class FrameAdmin(admin.ModelAdmin):
#     list_display = ('frame_code','maker', 'model_name', 'size', 'model_year', 'maker_url', 'created_datetime', 'updated_datetime')
#     list_display_links = ('frame_code', 'maker', 'model_name')

# admin.site.register(Frame, FrameAdmin)



# CSV管理
class FrameResource(resources.ModelResource):
    # Modelに対するdjango-import-exportの設定
    class Meta:
        model = Frame

@admin.register(Frame)
class FrameAdmin(ImportExportModelAdmin):
    # ImportExportModelAdminを利用するようにする
    ordering = ['frame_code']
    list_display = ('frame_code','maker', 'model_name', 'size', 'model_year', 'maker_url', 'created_datetime', 'updated_datetime')
    list_display_links = ('frame_code', 'maker', 'model_name')
    # django-import-exportsの設定
    resource_class = FrameResource
    


class Input_valuesResource(resources.ModelResource):
    # Modelに対するdjango-import-exportの設定
    class Meta:
        model = Input_values

@admin.register(Input_values)
class Input_valuesAdmin(ImportExportModelAdmin):
    # ImportExportModelAdminを利用するようにする
    ordering = ['frame_code']
    list_display = ('frame_code','seat_tube', 'seat_angle', 'top_tube', 'head_tube', 'head_angle', 'wheel_base', 'rear_senter', 'bb_drop','stack', 'reach')
    list_display_links = ('frame_code',)
    # django-import-exportsの設定
    resource_class = Input_valuesResource


class AccountResource(resources.ModelResource):
    # Modelに対するdjango-import-exportの設定
    class Meta:
        model = Account

@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    # ImportExportModelAdminを利用するようにする
    ordering = ['account_name']
    list_display = ('account_name','password', 'last_login_time', 'created_datetime', 'updated_datetime', )
    list_display_links = ('account_name',)
    # django-import-exportsの設定
    resource_class = AccountResource
    

