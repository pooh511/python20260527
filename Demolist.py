 # Demolist.py

#  리스트형식 연습
lst = [1,2,3,4,5]
print(len(lst))
lst.append(6)
print(lst)

# 삭제
lst.remove(3)
print(lst)


#문자열 슬라이싱
strA = "python" 
strB = "python is powerful"
strC = "when I save it as duplicate lines"
print(strA)
print(strB[0])
print(strB[1])
print(strB[0:3])
print(strB[0:3])

#형식 연습
a ={1,2,3,3}
b ={3,4,4,5}
print(a)
print(b)
print(len(b))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))


#tuple 연습
tp = (10,20,30)
print(len(tp))
print(tp[0])
print(tp.index(30))

#여러개를 리턴
def calc(a,b):
    return a+b,a*b
print(calc(3,4))
print("id: %s, name :%s" % ("kim","김유신"))


#형식변환
a = str((1,2,3))
print(a)
b=list(a)
b.append(4)
print(b)
