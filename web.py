#web.py
#크롤링을 위한 선언
from bs4 import BeautifulSoup

#연습용페이지 로딩
page = open("Chap09_test.html", "rt", encoding="utf-8").read()
#검색용 객체 생성
soup = BeautifulSoup(page, "html.parser")
#전체페이지
#print(soup.prettify()) #prettify=>전체문서를 보여줘 라는 명령어
#<p>태그로 선택하기
#태그 이름이 p인 요소를 모두 선택한다
#print(soup.find_all("p",attrs={"class": "outer-text"}))
# id 속성으로 선택하기
print(soup.find_all("p",attrs={"id": "first"}))

#<p>태그의 텍스트만 추출
for item in soup.find_all("p"):
    title = item.text.strip()
    #문자열을 가공
    title = title.replace("\n", "")
    
    print(title)


#문자열 형식의 메서드 설명
data = "<<< 치킨 피자 햄버거 >>>"
result = data.strip("<> ") #문자열의 양쪽에서 <,> 제거
print(data) 
print(result)

#import requests
#웹페이지의 HTML코드를 가져온다
#url = "https://www.naver.com"   
#response = requests.get(url)
#html = response.text    
#BeautifulSoup 객체로 변환한다
#soup = BeautifulSoup(html, 'html.parser')
#태그로 선택하기
#태그 이름이 a인 요소를 모두 선택한다
#a_tags = soup.select('a')
#print(a_tags)