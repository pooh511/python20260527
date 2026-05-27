#parent
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber
        
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))
              
#child
class Student(Person):#person 이라는 부모 클래스를 상속받고 추가 내용 덮어쓰기(subject,studentID)
    def __init__(self, name, phoneNumber, subject, studentID):
        
        #self.name = name
        #self.phoneNumber = phoneNumber
        super().__init__(name,phoneNumber)
        self.subject = subject
        self.studentID = studentID
        
    def printInfo(self):
        print(f"Info(Name: {self.name}, Phone Number: {self.phoneNumber})")
        print(f"Info(학과: {self.subject}, 학번: {self.studentID})")

p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "991122")
#print(p.__dict__)
#print(s.__dict__)
p.printInfo()
s.printInfo()

