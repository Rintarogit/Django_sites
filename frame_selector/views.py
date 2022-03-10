
from functools import reduce
from os import read
from django import forms
from django.forms.models import ALL_FIELDS
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
import sys
import csv
import shutil # コピーに使用
import os
from pathlib import Path
from decimal import Context, Decimal
import datetime


# アカウント認証関連


# もともとのメモアプリ
from .models import Memo
from .forms import  MemoForm


from .models import Input_values
from .forms import  Input_valuesForm
from .models import Frame
from .forms import  FrameForm
# アカウント
from .models import Account
from .forms import  AccountForm


#--------------------
# ログインチェック関数
#--------------------
def login_check(status):
  print('[def account_login]')
  try:
    result = Account.objects.get(account_name=status['username'],password=status['password'])
  except:
    result = 'False'

  return result


#-----------------------------
# aboutページ表示関数
#-----------------------------
def about(request):
  context = {}
  return render(request, 'frame_selector/about.html', context)


#-----------------------------
# Contactページ表示関数
#-----------------------------
def contact(request):
  context = {}
  if request.method == "POST":
    form = MemoForm(request.POST)
    if form.is_valid():
        form.save()
        context['message_e'] ='Thank you for your message!'
        context['message_j'] ='ご意見ありがとうございます！'
        return render(request, 'frame_selector/contact.html', context)
        # return redirect('frame_selector:contact')
  else:   
      form = MemoForm
  context = {'form': form}

  return render(request, 'frame_selector/contact.html', context)


#-----------------
# トップページ関数
#-----------------
def index(request):
  memos = Memo.objects.all().order_by('-updated_datetime')            # もともとのメモアプリであったやつ
  columns = []
  col_parts = ['cola','colb','colc','cold','cole','colf','colg','colh','coli','colj','colu',]
  context = {}
  print('+++++++++++++++++++ ' + str(request.POST))


  if request.method == "POST":
    # ------------
    # ログイン部分
    # ------------
    if 'logincheck' in request.POST :
      status = {}
      status = request.POST   # 関数に直接入れられないため変数に格納
      login_result = login_check(status)
      if login_result != 'False':
        context = {}
        form = Input_valuesForm(login_result)
        print('++++++++ログイン成功++++++++')
        context['form'] = form
        request.session['form_data'] = form
        return render(request, 'frame_selector/index.html', context)
    # --------------------------

    # else:
    # 元データだと操作不可のためコピーを作成
    input_data = (request.POST).copy()
    # フレームコードを無理やり追加
    input_data['frame_code'] = 'USER_INPUT_VALUES'
    form = Input_valuesForm(input_data)
    print('############# ' + str(input_data))
    # -----------------
    # 登録or上書き処理
    # -----------------
    if form.is_valid(): # 入力エラーがない場合

      # セッションにデータを格納(フォームに保持するため)
      request.session['form_data'] = request.POST 
      # アカウント不要の検索
      recommend_items = get_frame_list(input_data)

      # # 登録データあり
      # try:
      #   userrecord= Input_values.objects.get(frame_code=input_data['frame_code'])
      #   print('def index POST ' + str(userrecord) + ' 登録済み')
      #   form= Input_valuesForm(request.POST,instance=userrecord)
      # # 登録データなし
      # except Exception as e:
      #   print('def index POST 該当データなし {}'.format(type(e)))
      #   form = Input_valuesForm(request.POST)
      # finally:
      #   form.save()
      # # 上すっとばせない？？
      # recommend_items = get_frame_data(input_data['frame_code'])    # ユーザー入力データからおすすめフレームを算出

      if len(recommend_items) != 0:
        frame_total_items = []
        all_records       = Input_values.objects.all().order_by('frame_code')      # 辞書型でDB情報が欲しいため、object.getは使えない
        all_records_list  = list(all_records.values())

        for recommend_item in recommend_items:
          frame_code_item  = split_code(recommend_item['frame_code'])              # フレームコードを分離して情報を取得

          for  record in all_records_list:                                         # DB登録情報を取得
            if record['frame_code'] == recommend_item['frame_code']:
              table_item = record

          frame_total_item = {**table_item,**recommend_item,**frame_code_item}     # DB登録情報、差分、メーカー名を全てまとめる。
          frame_total_items.append(frame_total_item)

        context['form'] = form
        context['frames']  = frame_total_items
        context['memos'] = memos

        return render(request, 'frame_selector/index.html', context)

      return redirect('frame_selector:index')

  else: # POST意外
    # 前回データがあればそれを使う
    try:
      form = Input_valuesForm(request.session.get('form_data'))

    except:
      form = Input_valuesForm
    

  context['form']  = form
  context['memos'] = memos


  return render(request, 'frame_selector/index.html', context)

#-----------------------------
# 詳細ページ表示関数（idで管理）
#-----------------------------
def frame_detail(request, frame_id):
  context = {}
  context['frame_code_data'] = split_code(str(get_object_or_404(Input_values, id=frame_id)))
  context['frame_obj'] = get_object_or_404(Input_values, id=frame_id)

  return render(request, 'frame_selector/frame_detail.html', context)


def detail(request, memo_id):
  memo = get_object_or_404(Memo, id=memo_id)
  return render(request, 'frame_selector/detail.html', {'memo': memo})


#-------------------------------------------------------
# レコード検索関数(DB構成変更前に使用）
#-------------------------------------------------------
def get_record(model,item):
  item_list = []  # 引数格納用
  items     = []  # 検索結果格納変数

  print('def get_record item type is {}'.format(type(item)))

  if type(item) == list:
    item_list.extend(item)
  elif type(item) == str or type(item) == int:
    item_list.append(item)
  else:
    print('[ERROR] def get_record 引数に誤りがあります')
    return 
  for item in item_list:
    try:      
      items.append(model.objects.get(frame_code=item))
    except:
      pass
  return items


#--------------------------------------
# ジオメトリ差分計算関数(登録不必要版)
#--------------------------------------
def get_frame_list(values):
  print('def get_frame_list :{}'.format(values))
  recommend_frames = [] # おすすめフレームのコードをを格納する配列
  field_names      = []
  subtraction_dict = {}
  input_data       = values

  all_records      = Input_values.objects.all().order_by('frame_code')
  meta_fields      = Input_values._meta.get_fields()

  # フィールド名を取得
  for meta_field in meta_fields:
    if meta_field.name == 'id' or meta_field.name == 'frame_code':
      pass
    elif meta_field.name == 'maker_url':                  # フィールド順でURL以降は判定しない 
      break
    else:
      field_names.append(meta_field.name)

  #---差分計算処理---
  # アカウント登録する場合は改良が必要
  for record in all_records:
    if record.frame_code == 'USER_INPUT_VALUES':
      recommend_f = 'False'
      pass
    else:
      recommend_f      = 'True'                            # フラグを初期化
      subtraction_dict = {}                                # 差分保存変数を初期化
      subtraction_dict['frame_code'] = record.frame_code   # 辞書型にフレームコードを追加
      #---フィールドごとに計算---
      for field_name in field_names:
        subtract = 0                                       # 差分格納変数を初期化
        dif_field_name = 'dif_'+field_name
        if input_data.__getitem__(field_name) == '' or input_data.__getitem__(field_name) is None or record.__dict__[field_name] is None:        # 入力値がない場合(is Noneのときと''の時があるため)
          subtraction_dict[dif_field_name] = Decimal('0.00')
        else:
          d1 = str(input_data.__getitem__(field_name))     # 小数点以下で誤差が生じるため、
          d2 = str(record.__dict__[field_name])            # Decimal to Str to Decimal
          subtract = Decimal(d1)-Decimal(d2)
          subtraction_dict[dif_field_name] = -subtract

          if abs(subtract) >= 15:                          # 差分が大きかった場合フラグを変更
            recommend_f = 'False'
            subtraction_dict = {}                          # 辞書を初期化
            break;

    if recommend_f == 'True':
      recommend_frames.append(subtraction_dict)
  return recommend_frames



#----------------------------------------------------------------
# ジオメトリ差分計算関数 (アカウント登録パターン)
#----------------------------------------------------------------
def get_frame_data(user_name):
  print('def get_frame_data :{}'.format(user_name))
  recommend_frames = [] # おすすめフレームのコードをを格納する配列
  field_names      = []
  subtraction_dict = {}
  userrecord       = Input_values.objects.get(frame_code=user_name)
  all_records      = Input_values.objects.all().order_by('frame_code')
  meta_fields      = Input_values._meta.get_fields()

  # フィールド名を取得
  for meta_field in meta_fields:
    if meta_field.name == 'id' or meta_field.name == 'frame_code':
      pass
    elif meta_field.name == 'maker_url':                  # フィールド順でURL以降は判定しない 
      break
    else:
      field_names.append(meta_field.name)

  #---差分計算処理---
  for record in all_records:
    if record.frame_code == 'USER_INPUT_VALUES':
      recommend_f = 'False'
      pass
    else:
      recommend_f      = 'True'                            # フラグを初期化
      subtraction_dict = {}                                # 差分保存変数を初期化
      subtraction_dict['frame_code'] = record.frame_code   # 辞書型にフレームコードを追加
      #---フィールドごとに計算---
      for field_name in field_names:
        subtract = 0                                       # 差分格納変数を初期化
        dif_field_name = 'dif_'+field_name
        if userrecord.__dict__[field_name] is None or record.__dict__[field_name] is None:        # 入力値がない場合
          subtraction_dict[dif_field_name] = Decimal('0.00')
          # print('def get_frame_data UserInput [{}] is Null'.format(field_name))
        else:
          subtract = userrecord.__dict__[field_name] - record.__dict__[field_name] 
          subtraction_dict[dif_field_name] = -subtract

          if abs(subtract) >= 15:                          # 差分が大きかった場合フラグを変更
            recommend_f = 'False'
            subtraction_dict = {}                          # 辞書を初期化
            break;

    if recommend_f == 'True' :
      recommend_frames.append(subtraction_dict)
  return recommend_frames

#------------------------
# フレームコード分割関数
#------------------------
def split_code(code):
  data = {}
  split_items=code.split('_')
  print('split    : ' +str(split_items))
  data['maker'] = split_items[0]
  data['model_name'] = split_items[1]
  data['model_year'] = split_items[2]
  data['size'] = split_items[3]

  return data


#------------------------
# アカウント作成関数
#------------------------
def create_account(request):
  context = {}
  if request.method == "POST":
    form = AccountForm(request.POST)
    if form.is_valid():
        form.save()
        context['account_name'] = request.POST['account_name']
        print('AAAAAAA  ' + str(context['account_name']))
        return render(request, 'frame_selector/index.html', context)

  else:   
      form = AccountForm
  template_name = "frame_selector/create_account.html"
  context = {'form': form}

  return render(request,template_name,context)







#-------------------------------------------------------------------------
# DBデータのエクスポート関数
# ※ImportExportModelAdminの実装により不要になったため、現在使用していない
#-------------------------------------------------------------------------
def export_csv():
  print('def export_csv')
  status = 'False'
  try:
    model = Input_values
    d_today = datetime.date.today()
    field_names = []
    writeline = []

    all_data = Input_values.objects.all().order_by('frame_code')

    b_dir = os.path.dirname(os.path.abspath(__file__))
    with open(str(b_dir) + '/csv/data_backup{}.csv'.format(d_today),'w') as f:

      for field in model._meta.fields:  # フィールド名を取得（idのみ除外）
        if field.name !='id':
          field_names.append(field.name)

      f_writer = csv.DictWriter(f, fieldnames=field_names)
      f_writer.writeheader()
      writer = csv.writer(f, lineterminator='\n')

      for row in all_data:            # データ書き込み処理
        writeline = []
        if row.frame_code == 'USER_INPUT_VALUES':
          pass
        else:
          for i in range(len(field_names)-2):
            writeline.append(str(row.__dict__[field_names[i]]))
          writer.writerow(writeline)
    # インポート用バックアップファイルを上書き
    shutil.copy(str(b_dir) + '/csv/data_backup{}.csv'.format(d_today),str(b_dir) + '/csv/data_backup.csv')
    f.close()
    status = 'True'
  except:
    pass
  return status

#-------------------------------------------------------------------------
# DBデータのインポート関数
# ※ImportExportModelAdminの実装により不要になったため、現在使用していない
#-------------------------------------------------------------------------
def import_csv():
  
  status    = 'False'
  input_row = {}
  b_dir     = os.path.dirname(os.path.abspath(__file__))
  file_dir  = str(b_dir) + '/csv/data_backup.csv'
  # ファイル読込み
  with open(file_dir, 'r') as f:
    reader = csv.reader(f)
    for row in reader:      
      if len(row) == 0 or row[0] == 'USER_INPUT_VALUES':
        pass
      elif row[0] == 'frame_code':
        field_names = row
      else:
        #---Decimal変換処理(zipの後の辞書だと__dict__が使用できないためこの方法)---
        for i in range(1,11):
          try:
            if row[i] is None:
              row[i] = Decimal('0')
            else:
              row[i] = Decimal(row[i])
          except Exception as e:
              print('def import_csv Decimal変換処理ERROR: ' +str(row[0]) + str(e))
              return status
        #---変換終了---
        try: # 登録データあり
          record= Input_values.objects.get(frame_code=row[0])
          print('def import_csv ' + str(record) + ' 登録済み')
          input_row = dict(zip(field_names,row))   # csvの行データを辞書型に変更
          print('*********** ' + str(input_row))
          form= Input_valuesForm(input_row,instance=record)

        except Exception as e:# 登録データなし
          print('def import_csv 該当データなし {}'.format(type(e)))
          input_row = dict(zip(field_names,row))   # csvの行データを辞書型に変更
          form = Input_valuesForm(input_row)
          print('*********** ' + str(input_row))

        except:
          print('***def import_csv ERROR***')
          return status

        finally:
          form.save()
  f.close()
  status    = 'True'

  return status




# 以下、メモ系関数

def new_memo(request):
  if request.method == "POST":
    form = MemoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('frame_selector:index')

  else:   
      form = MemoForm
  template_name = "frame_selector/new_memo.html"
  context = {'form': form}

  return render(request,template_name,context)

def edit_memo(request, memo_id):
  memo = get_object_or_404(Memo, id=memo_id)
  if request.method == "POST":
      form = MemoForm(request.POST, instance=memo)
      if form.is_valid():
          form.save()
          return redirect('frame_selector:index')
  else:
      form = MemoForm(instance=memo)
  return render(request, 'frame_selector/edit_memo.html', {'form': form, 'memo':memo })



@require_POST   # 画面のボタンからPOSTされた場合のみ動作する（URL直接入力でメモが削除されたら困るため。） 
def delete_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id)
    memo.delete()
    return redirect('app:index')




  
  
  
  
  
  