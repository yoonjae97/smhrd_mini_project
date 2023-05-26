from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods, require_POST,require_safe

# Create your views here.
# @require_http_methods(['GET', 'POST'])
# def login(request):
#     if request.user.is_authenticated: # 로그인 된 사용자는 로그인 버튼을 볼 일 없다.
#         return redirect('index')
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)