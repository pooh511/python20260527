#클래스연습
class Person:
    # 초기화메서드
    def __init__(self):
        #멤버변수
        self.name= "default name"
    def print(self):
        print("My name is {0}".format(self.name))


#인스턴스 생성
p1 = Person()
p2 = Person()
p3 = Person()
p1.name = "전우치"
p3.name = "박보검"
#method call
p1.print()
p2.print()
p3.print()
