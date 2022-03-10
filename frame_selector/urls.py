from django.urls import path
from . import views

app_name = 'frame_selector'
urlpatterns = [
    path('', views.index, name='index'),    # topページ
    path('about', views.about, name='about'),   # aboutページ
    path('contact', views.contact, name='contact'),   # contactページ

    path('<int:memo_id>', views.detail, name='detail'),
    path('new_memo', views.new_memo, name='new_memo'),
    path('edit_memo/<int:memo_id>', views.edit_memo, name='edit_memo'),
    path('delete_memo/<int:memo_id>', views.delete_memo, name='delete_memo'),

    path('frame_detail/<int:frame_id>', views.frame_detail, name='frame_detail'),
    path('create_account', views.create_account, name='create_account'),

]
