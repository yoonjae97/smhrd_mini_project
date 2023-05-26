from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from res.resUtil import dictfetchall
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password
from common.CommonUtils import dictfetchall, commonPage
# Create your views here.
def main(request):
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    context = {
        'userid':userid,
        'memseq':memseq
    }
    return render(request, 'res/main.html', context)

def res_index(request, pg):
    cursor = connection.cursor()
    sql = "select count(*) from restaurant"
    cursor.execute(sql)
    totalCnt = int(cursor.fetchone()[0])
    
    search_tag = request.GET.get('search', '')
    cp = commonPage(totalCnt, pg, 10)

    sql = f"""
        select A.mem_seq, A.res_seq, A.res_name, A.res_score, A.res_hit, 
            to_char(A.res_wdate, 'yyyy-mm-dd') res_wdate, A.mem_id, num
        from 
        (
            select  A.mem_seq, A.res_seq, A.res_name, 
                    A.res_score, A.res_hit, 
                    A.res_wdate, B.mem_id,
                    row_number() over(order by A.res_hit desc) num,
                    ceil(row_number() over(order by A.res_hit desc)/10)-1 pg
            from restaurant A 
            left outer join member B on A.mem_seq=B.mem_seq
            where A.res_name like '%{search_tag}%' or
            B.mem_id like '{search_tag}'


            -- 검색 조건 필요할 경우에 여기에
        ) A
        where A.pg={pg}
    """
    
    cursor.execute(sql)
    
    resList = dictfetchall(cursor)
    print(resList)
    context = {}
    # 로그인
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    context['memseq'] = memseq
    context['userid'] = userid

    context['resList'] = resList
    context['commonPage'] = cp
    return render(request, "res/res_index.html", context)


def res_detail(request, res_seq):
    
    cursor = connection.cursor()

    sql = f"""update restaurant set res_hit = res_hit +1 where res_seq = {res_seq}"""
    cursor.execute(sql)

    sql = f"""
    select mem_seq, res_name, res_locate, res_phone, res_content,  res_score, res_hit, res_wdate
    from restaurant
    where res_seq = {res_seq}
    """
    cursor.execute(sql)
    resInfo = dictfetchall(cursor)[0]
    
    sql = f"""
    select res_item_title, res_item_content, res_item_pic, res_item_price
    from res_item
    where res_seq = {res_seq}
    """
    cursor.execute(sql)
    menuList = dictfetchall(cursor)


    sql = f"""
    SELECT mem.mem_id, rev.res_review_title, rev.res_review_content,
    rev.res_review_wdate, rev.res_review_rating
    FROM res_review rev
        JOIN restaurant res
        ON rev.res_seq = res.res_seq
    INNER JOIN member mem
        ON res.mem_seq = mem.mem_seq
    where res.res_seq = {res_seq}
    """
    cursor.execute(sql)
    reviewList = dictfetchall(cursor)
    memseq = request.session.get('mem_seq', '')

    # 로그인
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')

    return render(request, 'res/res_detail.html',  
                  {'resInfo':resInfo, "menuList":menuList, 'reviewList':reviewList, 'memseq': memseq, 'userid':userid})
    
def res_join_form(request):
    return render(request, 'res/res_join_form.html')

def res_join_save(request):

    mem_id = request.POST.get('mem_id')
    password = request.POST.get('pwd')
    age = request.POST.get('age')
    name = request.POST.get('name')
    cursor = connection.cursor()
    membertype = request.POST.get('membertype')

    sql = f"""
    insert into member (
    mem_seq, mem_id, mem_password, mem_google_id, mem_naver_id, mem_type, mem_age, mem_name, mem_wdate, mem_update)
    values(mem_seq.NEXTVAL, '{mem_id}', '{password}', 'N', 'N', 1, '{age}', '{name}', sysdate, sysdate)
    """  

    cursor.execute(sql)
    connection.commit()  
    return redirect('res:main')


def write(request):
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    context = {
        'userid':userid,
        'memseq':memseq
    }
    return render(request, 'res/res_write.html', context)

def write_save(request):
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    title = request.POST.get('title')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    content = request.POST.get('content')
# mem_seq 가져와야함 (작성자 회원정보에서)
    cursor = connection.cursor()
    sql = f"""
    insert into restaurant (res_seq, mem_seq, res_name, res_locate, res_phone, res_content, res_hit, res_wdate)
    values (res_seq.NEXTVAL,{memseq}, '{title}', '{address}', '{phone}', '{content}', 0, sysdate)
    
    """
    cursor.execute(sql)
    connection.commit()
    return redirect('res:index', pg=0)

from django.db.models import Q
from res.models import Member
def logon(request):
    if request.method == 'GET':
        return render(request, 'res:main')
    
    elif request.method == 'POST':
        userid = request.POST.get('logonid',None)
        password = request.POST.get('logonpw',None)
        res_data = {}
        
        cursor = connection.cursor()
        sql = f"""select mem_seq from member where mem_id = '{userid}'"""
        cursor.execute(sql)
        memdict = dictfetchall(cursor)
        mem_seq = memdict[0]['mem_seq']

        if not (userid and password):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        else:
            q1 = Q(mem_id=userid)
            q2 = Q(mem_password=password)

            if len(Member.objects.filter(q1 & q2)) > 0:
                request.session['user'] = userid
                request.session['mem_seq'] = mem_seq
                # request.set_cookie('user', userid)
                return redirect('res:main') 
            
            else:
                res_data['error'] = '비밀번호가 일치하지 않습니다'
            
            # 로그인 실패 및 오류메세지와 함께 응답
            return render(request, 'res:main', res_data)
        
def logout(request):
    del request.session['user']
    return redirect('res:main')
    
def deletepost(request):
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    context = {}
    context['userid'] = userid
    context['memseq'] = memseq
    cursor = connection.cursor()
    sql = f"""
    delete from restaurant where mem_seq = '{memseq}'"""
    cursor.execute(sql)
    connection.commit()
    messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
    return redirect("res:index", pg=0)

