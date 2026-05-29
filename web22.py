#web2.py
from bs4 import BeautifulSoup
#웹서버에 요청
import urllib.request
#정규포현식
import re

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
#file 로 저장
f = open("todayhumor.txt", "wt", encoding="utf-8" )

for i in range(1,11):
    url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)
    print(url)  
    #클리앙의 중고장터 주소 
    #data ='https://ohou.se/' + str(i)
    #웹브라우져 헤더 추가 
    #req = urllib.request.Request(data,
    #url ="https://www.clien.net/service/board/sold"
    #웹브라우져 헤더 추가
    req = urllib.request.Request(url,headers = hdr)
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, "html.parser")
    #제목과 링크를 추출한다(필터링 작업)
    list = soup.find_all("td", attrs={"class":"subject"})

    for tag in list:
        title = tag.find("a").text.strip()
        print(title)
        f.write(title + "\n") #파일에 저장  

f.close()




#선택한 블럭 주석 : ctrl + /
# <span class="subject_fixed" data-role="list-title-text" title=" 미개봉 " )아이폰 대공개) 아이폰 14 프로 맥스 256GB 팝니다."> 아이폰 대공개) 아이폰 14 프로 맥스 256GB 팝니다. </span>