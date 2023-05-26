def dictfetchall(cursor):
    columns = [ col[0].lower() for col in cursor.description]
    # cursor의 description의 각 필드 이름 정보 - 배열
    # columns <- ['id', 'title', 'contents', 'writer']
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# << < 1 2 3 4 5 6 7 8 9 10 > >>
# << : 첫 번째 페이지, 항상
# < : 현재 페이지로부터 앞으로 이동할 페이지가 잇는지
#     현재 9페이지 < 8 페이지
# 1, 2, 3 ... 10 첫 번째 그룹 : 1~10
#                두 번째 그룹 : 11~20
#                세 번째 그룹 : 21~30
# > : 현재 페이지로부터 뒤로 이동할 페이지가 잇는지
#     현재 9페이지 > 10 페이지
# >> 마지막 페이지

import math
class commonPage:
    # 페이징에 필요한 3가지 정보  (전체 데이터 개수, 현재페이지, 한페이지에 표시될 개수)
    # totalCnt : 전체 데이터 개수
    # pageSize : 한 페이지에 데이터를 몇건씩 보여줄거야
    # 전체 페이지 개수 : ceil(totalCnt / pageSize)     
    # 232/10 = 23.2 -> 올림 = 24페이지
    # curPage : 현재 페이지 
    # 파이썬에서 클래스 설계할 때 가급적 생성자에서 변수 만들기
    def __init__(self, totalCnt=1, curPage=0, pageSize=10):
        self.curPage = curPage
        self.totalCnt = totalCnt
        self.totalPage = math.ceil(totalCnt/pageSize) - 1
        print(self.totalPage)
        self.start = (self.curPage // pageSize)*10
        self.end = self.start + 10
        if self.end > self.totalPage:
            self.end = self.totalPage + 1
        
        if self.curPage >=1:   # 앞으로 이동 가능
            self.isPrev = True
            self.pre_page = self.curPage - 1
        else:     # 더 이상 앞으로 갈 수 없음
            self.isPrev = False
            self.pre_page = 0

        if self.curPage < self.totalPage:   # 뒤로 이동 가능
            self.isNext = True
            self.next_page = self.curPage + 1
        else:     # 더 이상 앞으로 갈 수 없음
            self.isNext = False
            self.pre_page = self.curPage 

        self.page_range = range(self.start, self.end)