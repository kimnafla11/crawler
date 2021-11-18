#json 파일형식 [{변수명 : 값}]
#외부 패키지를 파일에서 사용하기 위해 임포트
import os
import sys
import urllib.request
import datetime
import time
import json

#함수
#어느 위치에 있어도 상관없따
#def 함수명(매개변수)
#매개변수 != 코드에 있는 변수
#지역변수 : 함수 내에 있는 파라미터
#전역변수 : 코드에 있는 파라미터
#return이 있는 함수 -> 함수 결과값을 코드에 활용해야하는 경우
#return이 없는 함수 있음 -> 결과 없으면 수행하고 함수 종료
#한줄짜리 함수 : lambda 함수명 -> lambda함수는 동일 파일에서만 호출 가능
#.pym은 함수 파일 형식


def get_req_url(url) : #ID/PW보내는 함수
    req = urllib.request.Request(url)
    #Naver API 호출시 ID/PW를 header에 추가 후 전송
    req.add_header("X-Naver-Client-id",'3W0SU9AivPHNuMrrzy9k') #개인 API key
    req.add_header("X-Naver-Client-Secret",'AoWdV0HMNy') #개인 API 비번

    #예외처리 try - except
    # try: 에러 없을 때 실행
    # except try : 에러 시 실행
    # finally : 에러 상관없이 무조건 실행
    try :
        response = urllib.request.urlopen(req) 

        if(response.getcode() == 200): #200 코드 받으면 사이트 성공적으로 접속한거임
            print("URL Request Success 앙 ♡해피")
            return response.read().decode("utf-8") #인코딩을 utf-8로 변환

    except Exception as e: # 사이트 접속 못했을때
        #에러 종류 1. ID/PW가 잘못됨 2.json파일이 잘못됐다거나(없거나)
        print(e)
        print("error for URL 밍 ㅠ ")
        return None

def main() :
    node_name = ['news','blog','cafearticle'] # 리스트(참조형변수/자료형 섞어서 ㄱㄴ)
    sNode = '' #블로그/카페/뉴스 중 하나
    searchName = 'ataraxia'
    display_count = 100 #네이버 API에서 하루에 100개 제공하니까 100개 가쥬와

    for sNode in node_name: #3번 반복(node_name리스트에 변수 3개 들어있으니까)
        jsonResult = [] #리스트 변수 선언(초기화), 반복문 한 번 돌때마다 초기화 새롭게 ㅇㅇ??
        
        # searchName = 검색어, 1 = 시작 페이지
        jsonSearch = getNaverSearch(sNode, searchName,1,display_count)#겟네이버서치() 함수 호출 우리가 입력한 키워드로 접속하고 데이터를 가져오겠다는 것

        #jsonSearch!=None : 검색 된 내용이 있다면/jsonSearch['display']!=0 : 제이슨 파일 형식에 display라는 문구가 존재한다면 반복
        while((jsonSearch != None) and (jsonSearch['display'] != 0)):
            
            for post in jsonSearch['items']: #jsonSearch에 item문구 들어있을때까지 반복해
                getPostData(sNode, post, jsonResult)#겟포스트데이터()함수 호출, 매개변수로는 post, jsonResult(아까 선언한 리스트) 크롤링한 정보가 어떤게 있는지 가져와서 파일에 저장하도록 만드는 함수
                
            nStart = jsonSearch['start']+jsonSearch['display'] # jsonSearch변수에서 start, display 내용 가져옴
            jsonSearch = getNaverSearch(sNode, searchName, nStart, display_count)
            
        with open('%s_naver_%s.json' %(searchName,sNode),'w',encoding='utf-8') as outfile : #json파일에 작성하는 부분, jsonResult에 저장된 데이터를 기반으로 정렬, utf-8로 저장하려고 아스키는 false값 지정
            retJson = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii = False)
            outfile.write(retJson)

        print('%s_naver_%s.json SAVED' %(searchName, sNode ))


########################

def getNaverSearch(sNode, searchName, start_Page, display_count):
#매개변수
#sNode : 리스트 중 하나 돌 때['뉴스','블로그','카페']
#searchName : 검색어
#start_page : 시작 페이지
#display_count : 출력 개수
    base = 'https://openapi.naver.com/v1/search/' #Naver API에서 사용하는 공통 url선언
    node = '%s.json' %(sNode) #[카페,블로그,뉴스] 값이 자꾸 바뀔테니가 잘 명시 시키기 위함, 문자열 포맷팅%할때 매칭되는 변수를 꼭 %붙여서 적어주기.
    parameters = "?query=%s&start=%s&display=%s" %(urllib.parse.quote(searchName), start_Page, display_count)
    #네이버API에서 원하는 키워드를 받아오기위한 파라미터 설정(순서 바뀌어도 상관없음)
    #urllib.parse.quote(search_text): 띄어쓰기와 머 따옴표 같은거 정제하기 위한 함수
    #질문??? start_Page, display_count는 API설명에서 정수형이라고 나와잇는데 문자형인지 궁금 --> 상관없음

    url = base+node+parameters

    regData = get_req_url(url) #get_req_url을 호출해서, 앞서 선언한 url변수 보냄, 정상적으로 값을 받아오는지 확인하는 부분

    if(regData == None): #값을 못받으면 None리턴(정상적으로 접속 안되면), getNaverSearch()호출된 부분에 None리턴
        return None
    else: #정상적으로 접속 됐으면 리턴
        return json.loads(regData) #regData를 리턴하지만 json파일형태로 변환해서 리턴한다.

#########################

def getPostData(sNode, post, jsonResult) :
    org_link = ''

    title = post['title'] #제목
    link = post['link'] #url정보
    description = post['description'] #설명글
    #total = post['total'] #결과 수 (위에 네 변수는 공통적 변수)

    if(sNode == 'news'):
        org_link = post['originallink']
        link = post['link']
        #total = post['total']

        #네이버 API에서 보내지는 pubDate형태를 형식에 맞게 변경하기 위한 부분
        pDate = datetime.datetime.strptime(post['pubDate'],'%a, %d %b %Y %H:%M:%S +0900')
        pDate = pDate.strftime("%Y-%m-%d %H:%M:%S")

        #네이버 API에서 보낸 값을 변수로 변경하여 jsonResult파일에 내용 추가
        jsonResult.append({'title': title, 'description':description, 'org_link':org_link, 'link':org_link, 'pDate':pDate}) #딕셔너리 참조형변수 형태임 ㅇㅇ

    elif(sNode == 'blog'):
        bloggername = post['bloggername']
        postdate = post['postdate']
        bloggerlink = post['bloggerlink']
            #total
            #jsonResult.append(['title':title, 'discription':discription, 'bloggername':bloggername, 'bloggerlink':bloggerlink, 'postDate':postDate])
        jsonResult.append({'title':title, 'description':description, 'bloggername':bloggername, 'bloggerlink':bloggerlink, 'postdate':postdate})

    else :
        cafename = post['cafename']
        cafeurl = post['cafeurl']
        link = post['link']
        jsonResult.append({'title':title, 'description':description, 'cafename':cafename, 'cafeurl':cafeurl, 'link':link})


if __name__ == "__main__":
    main()
