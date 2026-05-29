import requests
from bs4 import BeautifulSoup

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&ssc=tab.news.all&query=%EB%B0%98%EB%8F%84%EC%B2%B4&oquery=&tqi=jmQf0wqXKZGssECwRKl-162618&ackey=l64amp8z"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 네이버 뉴스 제목 영역에서 제목 링크 추출
titles = []

for a in soup.select("a.news_tit"):
    title = a.get_text(strip=True)
    if title:
        titles.append(title)

print("뉴스 제목 수:", len(titles))
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")