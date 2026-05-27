# 내장라이브러리.py

import random
print(random.random())
print(random.random())
#구간지정
print(random.uniform(2.0,5.0))
print(random.uniform(2.0,5.0))

#list 에서 무작위로 하나 뽑기
items =["apple","banana","cherry","date","fig","grape fruit"]

print(random.choice(items))

print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])

#로또번호
print(random.sample(range(1,46),6))
print(random.sample(range(1,46),6))
print(random.sample(range(1,46),6))

#파일명 다루기
import os.path


filename = "C:\Python313\python.exe"

print(os.path.basename(filename))
print(os.path.abspath("python.exe"))
print("환경변수:", os.environ)

if os.path.exists(filename):
    print("파일의크기:(0)".format(os.path.getsize(filename)))
    
else:
    print("파일이 존재하지 않습니다.") 



#특정 폴더에 파일 리스트 출력
import glob
print(glob.glob("C:\\work\\*.*"))

for item in glob.glob("C:\\work\\*.py"):
    print(item) 