# 파일 객체 생성
f = open("test.txt","wt",encoding="utf-8")#쓰기모드로 파일열기
f.write("첫번째라인\n 두번째라인\n 세번째라인\n")#파일에 문자열 쓰기
f.close()

# 파일 읽기
f = open("test.txt","tr",encoding="utf-8")#읽기모드로 파일열기
content = f.read()#파일 전체 내용 읽기
print(content)#읽은 내용 출력
f.close()#파일 닫기
