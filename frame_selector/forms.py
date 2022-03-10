from cProfile import label
from django.forms import ModelForm
from django import forms
from .models import Memo
from .models import Input_values
from .models import Frame
from .models import Account


class MemoForm(ModelForm):
    class Meta:
        model = Memo
        fields = ['title', 'text']
        labels={
            'title':'Title',
            'text' :'Message'
        }
# ModelFormのフィールドをhidden属性にして、フレームコードの入力を不要とする。
class Input_valuesForm(ModelForm):
    class Meta:
        model = Input_values
        fields = ['seat_tube', 'seat_angle', 'top_tube', 'head_tube', 'head_angle', 'wheel_base', 'rear_senter', 'bb_drop', 'stack', 'reach']
        labels={
                'seat_tube':'[A]Seat tube',
                'seat_angle':'[B]Seat angle',
                'top_tube':'[C]Top tube',
                'head_tube':'[D]Head tube',
                'head_angle':'[E]Head angle',
                'wheel_base':'[F]Wheel base',
                'rear_senter':'[G]Rear senter',
                'bb_drop':'[H]BB drop',
                'stack':'[I]Stack',
                'reach':'[J]Reach',
                }

#　現状直接入力することはないが、念のため作成
class FrameForm(ModelForm):
    class Meta:
        model = Frame
        fields = ['frame_code', 'maker', 'model_name', 'size', 'model_year', 'maker_url',]

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['account_name', 'password']