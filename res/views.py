from django.shortcuts import render, redirect, HttpResponse
from django.db import connection
from res.resUtil import dictfetchall
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password
from common.CommonUtils import dictfetchall, commonPage

# Create your views here.
# 메인 페이지
# django에서 session 값을 저장해두는 공간이 필요한데
# 처음 django-admin startproejct 하고 migrate를 한번도 하지 않으면
# 저장해줄 공간이 없다고 나옴
# 따라서 models.py와 관계없이 기본적으로 migrate가 한번 이루어져야함
def main(request):
    userid = request.session.get('user', '') # 메인 페이지 불러올 때 세션에 user(로그인한 아이디) 할당
    memseq = request.session.get('mem_seq', '') # 메인 페이지 불러올 때 세션에 mem_seq(로그인한 사람 seq) 할당
    context = {
        'userid':userid,
        'memseq':memseq
    }
    return render(request, 'res/main.html', context)

# 게시글 리스트 페이지
def res_index(request, pg):
    cursor = connection.cursor()
    sql = "select count(*) from restaurant"
    cursor.execute(sql)
    totalCnt = int(cursor.fetchone()[0])
    
    search_tag = request.GET.get('search', '')
    cp = commonPage(totalCnt, pg, 10)

    # 리스트 불러오고 페이징 처리
    # where문에 조건 2개 사용한 or 이 아닌
    # select 문 2개 생성 후 각각 where 조건을 주고 UNION으로 합쳤다면 
    # 검색 쿼리가 정상적으로 작동했을지도?
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
    
    # sql을 활용하여 가져온 게시글 리스트 할당
    resList = dictfetchall(cursor)
    context = {}

    # 로그인 상태를 구분할 수 있도록 세션에 값 할당
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    context['memseq'] = memseq
    context['userid'] = userid

    context['resList'] = resList
    context['commonPage'] = cp
    return render(request, "res/res_index.html", context)

# 게시글 상세 페이지
def res_detail(request, res_seq):
    
    cursor = connection.cursor()

    # 게시글 클릭 시 조회수 1씩 증가하는 쿼리
    sql = f"""update restaurant set res_hit = res_hit +1 where res_seq = {res_seq}"""
    cursor.execute(sql)

    # 가게의 상세정보를 위한 가게 1개 조회
    sql = f"""
    select mem_seq, res_name, res_locate, res_phone, res_content,  res_score, res_hit, res_wdate
    from restaurant
    where res_seq = {res_seq}
    """
    cursor.execute(sql)
    resInfo = dictfetchall(cursor)[0]
    
    # 가게의 메뉴 조회
    sql = f"""
    select res_item_title, res_item_content, res_item_pic, res_item_price
    from res_item
    where res_seq = {res_seq}
    """
    cursor.execute(sql)
    menuList = dictfetchall(cursor)

    # 가게에 작성한 리뷰들 조회
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
    
# 회원가입 페이지로 이동
def res_join_form(request):
    return render(request, 'res/res_join_form.html')

# 회원가입 데이터 저장 쿼리
def res_join_save(request):

    mem_id = request.POST.get('mem_id')
    password = request.POST.get('pwd')
    age = request.POST.get('age')
    name = request.POST.get('name')
    cursor = connection.cursor()

    sql = f"""
    insert into member (
    mem_seq, mem_id, mem_password, mem_google_id, mem_naver_id, mem_type, mem_age, mem_name, mem_wdate, mem_update)
    values(mem_seq.NEXTVAL, '{mem_id}', '{password}', 'N', 'N', 1, '{age}', '{name}', sysdate, sysdate)
    """  

    cursor.execute(sql)
    connection.commit()  
    # redirect 사용시 세션값을 지정해줄 필요 x
    return redirect('res:main')

# 글쓰기 페이지로 이동
def write(request):
    userid = request.session.get('user', '')
    memseq = request.session.get('mem_seq', '')
    context = {
        'userid':userid,
        'memseq':memseq
    }
    return render(request, 'res/res_write.html', context)

# 게시글 작성 
def write_save(request):

    # 게시글 작성자가 필요하므로 mem_seq 가져와야함 (작성자 회원정보에서)
    memseq = request.session.get('mem_seq', '')
    title = request.POST.get('title')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    content = request.POST.get('content')

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
# 로그인
def logon(request):
    # GET 방식으로 접근할 경우 로그인 안받음
    if request.method == 'GET':
        return render(request, 'res:main')
    
    # POST 방식으로 접근하면 입력한 로그인과 비밀번호 받기
    elif request.method == 'POST':
        userid = request.POST.get('logonid',None)
        password = request.POST.get('logonpw',None)
        res_data = {}
        
        # 테이블에는 중복값을 허용하지만 원래는 아이디가 중복 불가이므로 아이디로 
        # 회원정보 조회
        cursor = connection.cursor()
        sql = f"""select mem_seq from member where mem_id = '{userid}'"""
        cursor.execute(sql)
        memdict = dictfetchall(cursor)
        # [{데이터}] 형태이므로 인덱싱
        mem_seq = memdict[0]['mem_seq']

        if not (userid and password):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        else:
            # 아이디와 비밀번호가 일치하는 데이터를 찾기 위해 검색 조건 생성
            q1 = Q(mem_id=userid)
            q2 = Q(mem_password=password)

            # 아이디, 비밀번호 둘 다 일치하는 데이터가 존재할 때
            # 세션에 값 할당함
            if len(Member.objects.filter(q1 & q2)) > 0:
                request.session['user'] = userid
                request.session['mem_seq'] = mem_seq
                # request.set_cookie('user', userid)
                return redirect('res:main') 
            
            else:
                res_data['error'] = '정보가 일치하지 않습니다'
            
            # 로그인 실패 및 오류메세지와 함께 응답
            return render(request, 'res:main', res_data)
        
# 로그아웃 버튼을 누를 경우 세션 값 삭제함
def logout(request):
    del request.session['user']
    return redirect('res:main')

# 게시글 삭제
# 그대로 실행시 게시글을 모두 삭제함
# 추가로 게시글 title을 불러와서 where문 조건에 추가 필요할 듯
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

