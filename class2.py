# class2.py

# 사람(Person)의 정보를 담는 기본 클래스입니다.
# 아이디(id)와 이름(name)을 저장하고 출력해줍니다.
class Person:
    def __init__(self, id, name):
        # self.id는 이 객체가 가진 아이디 값을 기억합니다.
        self.id = id
        # self.name은 이 객체가 가진 이름 값을 기억합니다.
        self.name = name

    def printInfo(self):
        # 이 메서드는 저장된 정보를 화면에 보여줍니다.
        print("--- Person 정보 ---")
        print("ID:", self.id)
        print("이름:", self.name)


# 관리자(Manager)는 사람(Person)의 기능을 그대로 가지고,
# 추가로 직책(title)을 더 가집니다.
class Manager(Person):
    def __init__(self, id, name, title):
        # Person 클래스의 초기화 코드를 먼저 실행해서 id와 name을 설정합니다.
        super().__init__(id, name)
        # self.title은 이 관리자가 가진 직책을 기억합니다.
        self.title = title

    def printInfo(self):
        # Person의 정보를 먼저 출력하고, 추가로 직책도 보여줍니다.
        print("--- Manager 정보 ---")
        print("ID:", self.id)
        print("이름:", self.name)
        print("직책:", self.title)


# 직원(Employee)은 사람(Person)의 기능을 그대로 가지고,
# 추가로 기술(skill)을 더 가집니다.
class Employee(Person):
    def __init__(self, id, name, skill):
        # Person 클래스의 초기화 코드를 먼저 실행해서 id와 name을 설정합니다.
        super().__init__(id, name)
        # self.skill은 이 직원이 가진 기술을 기억합니다.
        self.skill = skill

    def printInfo(self):
        # Person의 정보를 먼저 출력하고, 추가로 기술도 보여줍니다.
        print("--- Employee 정보 ---")
        print("ID:", self.id)
        print("이름:", self.name)
        print("기술:", self.skill)


# 아래에서 총 10개의 인스턴스를 생성합니다.
# Person 4개, Manager 3개, Employee 3개를 만들어서 출력합니다.
people = [
    Person(1, "철수"),
    Person(2, "영희"),
    Person(3, "민수"),
    Person(4, "수지"),
    Manager(5, "철민", "부장"),
    Manager(6, "영아", "과장"),
    Manager(7, "현우", "차장"),
    Employee(8, "지우", "파이썬"),
    Employee(9, "하윤", "디자인"),
    Employee(10, "도윤", "데이터 분석"),
]

# 생성된 각 객체에 대해 printInfo()를 호출해서 정보를 차례대로 출력합니다.
for person in people:
    person.printInfo()
    print()
