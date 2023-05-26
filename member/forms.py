from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


class CreateMemberForm(UserCreationForm):
    CHOICES=[('1', '일반 회원'),('2','사장님 회원'),('3',)]
    
    isgeneral = forms.ChoiceField(
        label = '회원유형',
        choices = CHOICES,
        widget = forms.RadioSelect,
        required=True
    )
    
    username = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
            'class': 'my-username form-control',
            'placeholder': '사용자 이름을 입력하세요',
            'style' : 'width:300px;'
            },
	    )   
	)
    
    birthday = forms.DateField(
        label='생년월일',
        widget=forms.NumberInput(
            attrs={
            'type':'date',
            'class': 'my-birthday form-control',
            'placeholder': '생년월일을 입력해주세요',
            'style' : 'width:300px;'
            }
        ),
	)
    class Meta(UserCreationForm.Meta):
        model = get_user_model() #user
        fields = UserCreationForm.Meta.fields + ('isgeneral', 'birthday')
