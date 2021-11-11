#json 파일형식 [{변수명 : 값}]
#외부 패키지를 파일에서 사용하기 위해 임포트
import os
import sys
import urllib.request
import datetime
import time
import json

#함수
#def 함수명(매개변수)
#매개변수 != 코드에 있는 변수
#지역변수 : 함수 내에 있는 파라미터
#전역변수 : 코드에 있는 파라미터
#return이 있는 함수 -> 함수 결과값을 코드에 활용해야하는 경우
#return이 없는 함수 있음 -> 결과 없으면 수행하고 함수 종료
#한줄짜리 함수 : lambda 함수명 -> lambda함수는 동일 파일에서만 호출 가능
#.pym은 함수 파일 형식

def get_req_url(url) : #ID/PW보내는 함수
    req = urllib.request.Response(url)
    #Naver API 호출시 ID/PW를 header에 추가 후 전송
    req.add_header("X-Naver-Client-id",'3W0SU9AivPHNuMrrzy9k') #개인 API key
    req.add_header("X-Naver-Client-Secret",'AoWdV0HMNy') #개인 API 비번

    #예외처리 try - except
    # try: 에러 없을 때 실행
    # except try : 에러 시 실행
    # finally : 에러 상관없이 무조건 실행
    try :
        response = urllib.request.urlopen(req) 

        if(response.getCode == 200): #200 코드 받으면 사이트 성공적으로 접속한거임
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
    display_count = 100 #네이버 API에서 하루에 100개 제공하니까 100개 가쥬와

    for sNode in node_name: #3번 반복(node_name리스트에 변수 3개 들어있으니까)
        jsonResult = [] #리스트 변수 선언(초기화), 반복문 한 번 돌때마다 초기화 새롭게 ㅇㅇ??
        
        # searchName = 검색어, 1 = 시작 페이지
        jsonSearch = getNaverSearch(sNode, searchName,1,display_count)#겟네이버서치() 함수 호출

        #jsonSearch!=None : 검색 된 내용이 있다면/jsonSearch['display']!=0 : 제이슨 파일 형식에 display라는 문구가 존재한다면 반복
        while((jsonSearch ! = None) and (jsonSearch['display'] != 0)):
            
            for post in jsonSearch['item']: #jsonSearch에 item문구 들어있을때까지 반복해
                getPostData(sNode, post, jsonResult)#겟포스트데이터()함수 호출, 매개변수로는 post, jsonResult(아까 선언한 리스트)
                
            nStart = jsonSearch['start']+jsonSearch['display'] # jsonSearch변수에서 start, display 내용 가져옴
            jsonSearch = getNaverSearchResult(sNode, search_text, nStart, display_Count)
            
        with open('파일 저장할 위치 입력') as outfile : #json파일에 작성하는 부분, jsonResult에 저장된 데이터를 기반으로 정렬, utf-8로 저장하려고 아스키는 false값 지정
            retJson = json.dumps(jsonResult, indent = 4, sort_key = True, ensure_ascii = False)
            outfile.write(retJson)

if "__name__" == "__main__":
    url = 'https://openapi.naver.com/v1/search/'
    get_req_url(url)
