# 함수연습

#1)함수정의
def setvalue(netValue):
    x = netValue
    print("함수내부",x)

#2)함수를호출
netValue = setvalue(5)
print(netValue)

#값을 리턴하는 함수
def swap(a,b):
    return b,a

#호출
netValue = swap(3,4)
print(netValue)
#전역변수
x =5
def func(a):
    return a+x

#기본값을명시
def times(a=10,b=20):
    return a*b

print(times())
print(times(5))
print(times(5,6))

def connectURI(server,port):
    strURL= "https"+server+":"
    return strURL

#호출
print(connectURI("multi.com","80"))
print(connectURI(port="8080",server="naver.com"))


#디버깅예시
def union(*ar):

    result =[]
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)

                return result

print(union("ham","egg"))
print(union("ham","egg","spam,"))


#lambda호출
g = lambda x,y:x*y
print(g(3,4))
print(g(5,6))
print((lambda x:x*x)(3))

print((lambda y:x*y)(3))
print(dir())
print(globals())
