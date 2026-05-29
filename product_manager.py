# 필요한 라이브러리들을 불러오기
# sqlite3: 데이터베이스를 쉽게 관리하는 도구 (파일 형태의 작은 데이터베이스)
import sqlite3

# datetime: 시간과 날짜를 다루는 도구 (얼마나 걸렸는지 시간을 재기 위해 사용)
from datetime import datetime

# random: 무작위로 뽑기 (주사위 굴리기 같은 것) - 샘플 데이터를 만들 때 사용
import random

# ========== 🎯 제품 데이터베이스를 관리하는 클래스 정의 ==========
# 클래스는 관련된 기능들을 하나로 묶어둔 것
# 마치 장난감 상자 안에 장난감 여러 개를 함께 넣어두는 것처럼!
class ProductManager:
    """
    SQLite를 사용한 제품 데이터베이스 관리 클래스
    
    설명: 이 클래스는 마치 '편의점 점장'처럼 생각할 수 있습니다.
    상품을 추가하고, 수정하고, 삭제하고, 검색할 수 있습니다.
    """
    
    def __init__(self, db_name="MyProduct.db"):
        """
        데이터베이스 초기화 - 처음 시작할 때 자동으로 실행됩니다
        
        설명: 생일파티를 준비하기 전에 풍선을 부풀리고 방을 정리하는 것처럼,
        데이터베이스를 사용할 준비를 합니다.
        
        매개변수 (파라미터):
            db_name: 데이터베이스 파일 이름 (기본값: "MyProduct.db")
                    예: "MyProduct.db" → 이 이름으로 파일이 생성됩니다
        """
        # 데이터베이스 파일 이름을 저장해두기 (나중에 사용할 때를 위해)
        self.db_name = db_name
        
        # 데이터베이스와 연결할 통로를 준비해두기 (처음엔 비어있음)
        self.connection = None
        
        # 데이터베이스에 명령을 내릴 도구를 준비해두기 (처음엔 비어있음)
        # cursor = 마치 마우스 커서처럼 데이터베이스 안에서 움직이면서 일을 합니다
        self.cursor = None
        
        # 데이터베이스에 실제로 연결하기 (아래에 정의된 connect() 함수 실행)
        self.connect()
        
        # 상품 정보를 저장할 테이블 만들기 (아래에 정의된 create_table() 함수 실행)
        self.create_table()
    
    def connect(self):
        """
        데이터베이스에 실제로 연결하기
        
        설명: 마치 전화를 걸어서 편의점과 연결하는 것처럼,
        컴퓨터가 데이터베이스 파일과 연결합니다.
        
        try ~ except: 무언가 잘못되었을 때를 대비한 안전장치
                    마치 안전벨트처럼 문제가 생겨도 안전하게 처리합니다
        """
        try:
            # 🔌 데이터베이스 파일과 연결하기 (전화를 거는 것처럼)
            # sqlite3.connect(): SQLite 데이터베이스와 연결하는 함수
            self.connection = sqlite3.connect(self.db_name)
            
            # 🎮 데이터베이스를 조작할 도구 준비하기 (리모콘처럼)
            # cursor: 데이터베이스에 명령을 내릴 수 있는 도구
            self.cursor = self.connection.cursor()
            
            # 연결 성공 메시지 출력 (성공했다고 알려주기)
            print(f"✓ 데이터베이스 '{self.db_name}' 연결 완료")
        
        # 만약 연결에 실패하면 이 부분이 실행됩니다 (안전장치 작동!)
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 실패: {e}")
    
    def create_table(self):
        """
        상품 정보를 저장할 테이블 만들기
        
        설명: 마치 '엑셀 스프레드시트'처럼 행과 열로 된 표를 만듭니다.
        이 표에 상품의 ID, 이름, 가격 정보를 저장합니다.
        
        테이블 구조:
        ┌─────────────┬──────────────┬───────────────┐
        │ productID   │ productName  │ productPrice  │
        ├─────────────┼──────────────┼───────────────┤
        │ 1           │ "스마트폰"   │ 1000000       │
        │ 2           │ "노트북"     │ 1500000       │
        └─────────────┴──────────────┴───────────────┘
        """
        try:
            # 🗂️ SQL 명령으로 테이블 만들기
            # SQL: 데이터베이스와 대화하는 언어 (데이터베이스 전용 말)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY AUTOINCREMENT,
                    -- 상품 고유번호: 자동으로 1, 2, 3... 증가합니다
                    
                    productName TEXT NOT NULL,
                    -- 상품 이름: 글자(텍스트) 형태이고, 반드시 입력해야 합니다
                    
                    productPrice INTEGER NOT NULL
                    -- 상품 가격: 숫자(정수) 형태이고, 반드시 입력해야 합니다
                )
            ''')
            
            # 💾 변경사항을 데이터베이스에 저장하기 (마치 파일을 저장하는 것처럼)
            # commit: "확실히 저장해!" 이라고 명령하는 것
            self.connection.commit()
            
            # 테이블 생성 성공 메시지 출력
            print("✓ Products 테이블 준비 완료")
        
        # 만약 테이블 만드는 것이 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 실패: {e}")
    
    def insert(self, product_name, product_price):
        """
        새로운 상품 하나를 데이터베이스에 추가하기
        
        설명: 마치 편의점 진열대에 새로운 상품을 하나씩 놓는 것처럼,
        데이터베이스 테이블에 새로운 행을 추가합니다.
        
        매개변수 (파라미터):
            product_name: 상품 이름 (예: "스마트폰", "노트북")
            product_price: 상품 가격 (예: 1000000, 1500000)
        
        반환값:
            새로 추가된 상품의 ID 번호 (예: 1, 2, 3...)
            실패하면 None 반환
        """
        try:
            # 📝 새로운 상품 정보를 테이블에 추가하는 SQL 명령
            # INSERT: "넣다" 라는 뜻의 SQL 명령
            # INTO Products: Products 테이블에 넣어라
            # VALUES (?, ?): 물음표(?) 자리에 값을 넣어주세요
            self.cursor.execute('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', (product_name, product_price))
            # (product_name, product_price): 실제로 넣을 값들
            
            # 💾 변경사항을 데이터베이스에 저장하기
            self.connection.commit()
            
            # ✨ 새로 추가된 상품의 ID 번호 반환하기
            # lastrowid: 마지막으로 추가된 행의 ID 번호
            return self.cursor.lastrowid
        
        # 만약 상품 추가가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 삽입 실패: {e}")
            return None  # None: "실패했어" 라는 의미
    
    def insert_many(self, products_list):
        """
        여러 개의 상품을 한 번에 데이터베이스에 추가하기
        
        설명: 마치 편의점에 여러 상자의 상품을 한 번에 배송받아서
        진열대에 놓는 것처럼, 많은 상품들을 한 번에 추가합니다.
        
        매개변수 (파라미터):
            products_list: 상품 정보 여러 개가 들어있는 리스트
                          예: [("스마트폰", 1000000), ("노트북", 1500000), ...]
        
        반환값:
            성공하면 True, 실패하면 False
        """
        try:
            # 🚀 여러 개의 상품을 한 번에 추가하는 SQL 명령
            # executemany: "여러 번 실행해!" 라는 뜻
            # 마치 "한 번에 여러 개씩 넣어" 라는 의미
            self.cursor.executemany('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', products_list)
            # products_list: 여러 개의 (이름, 가격) 쌍이 들어있는 리스트
            
            # 💾 변경사항을 데이터베이스에 저장하기
            self.connection.commit()
            
            # ✅ 몇 개의 상품을 추가했는지 알려주기
            # len(products_list): 리스트의 길이 = 추가한 상품의 개수
            print(f"✓ {len(products_list)}개 데이터 삽입 완료")
            
            # 성공을 나타내는 True 반환
            return True
        
        # 만약 대량 추가가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 대량 데이터 삽입 실패: {e}")
            return False  # 실패를 나타내는 False 반환
    
    def select_all(self):
        """
        데이터베이스의 모든 상품 정보를 가져오기
        
        설명: 마치 편의점 진열대 전체를 쭉 둘러보는 것처럼,
        데이터베이스에 저장된 모든 상품의 정보를 가져옵니다.
        
        반환값:
            모든 상품의 정보를 담은 리스트
            예: [(1, "스마트폰", 1000000), (2, "노트북", 1500000), ...]
            실패하면 빈 리스트 [] 반환
        """
        try:
            # 🔍 모든 상품 정보를 가져오는 SQL 명령
            # SELECT *: "모든 것을 선택해" 라는 뜻
            # *: "별" 기호는 "모든 것" 을 의미
            # FROM Products: "Products 테이블에서"
            self.cursor.execute('SELECT * FROM Products')
            
            # 📋 조회한 결과를 모두 가져오기
            # fetchall(): 모든 결과를 리스트 형태로 가져오는 함수
            results = self.cursor.fetchall()
            
            # 결과 반환하기
            return results
        
        # 만약 조회가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []  # 빈 리스트 반환 (아무것도 없음)
    
    def select_by_id(self, product_id):
        """
        특정 ID 번호를 가진 상품 정보를 가져오기
        
        설명: 마치 편의점에서 "123번 상품이 뭐야?" 라고 물어보는 것처럼,
        특정 ID 번호의 상품 정보만 가져옵니다.
        
        매개변수 (파라미터):
            product_id: 찾을 상품의 ID 번호 (예: 1, 5, 10...)
        
        반환값:
            해당 ID의 상품 정보 (예: (1, "스마트폰", 1000000))
            없으면 None 반환
        """
        try:
            # 🔍 특정 ID를 가진 상품을 찾는 SQL 명령
            # SELECT *: "모든 정보를 선택해"
            # WHERE productID = ?: "상품 ID가 ?와 같은 것만"
            # WHERE: "어디서" - 조건을 지정하는 키워드
            self.cursor.execute('SELECT * FROM Products WHERE productID = ?', (product_id,))
            # (product_id,): 물음표(?) 자리에 들어갈 값
            
            # 📋 조회한 결과를 하나만 가져오기
            # fetchone(): 한 개의 결과만 가져오는 함수 (첫 번째 것만)
            result = self.cursor.fetchone()
            
            # 결과 반환하기
            return result
        
        # 만약 조회가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return None  # None: "없어" 또는 "찾을 수 없어"
    
    def select_by_name(self, product_name):
        """
        상품 이름으로 찾기 (부분일치 검색)
        
        설명: 마치 편의점에서 "스마트폰이라는 이름을 가진 상품 보여줘" 라고 물어보는 것처럼,
        상품 이름에 해당 글자가 포함된 모든 상품을 찾습니다.
        
        매개변수 (파라미터):
            product_name: 찾을 상품 이름의 일부 (예: "스마트폰")
        
        반환값:
            해당 이름을 포함하는 모든 상품의 정보 리스트
            예: [(1, "스마트폰", 1000000), (5, "스마트폰2", 1200000), ...]
            없으면 빈 리스트 [] 반환
        """
        try:
            # 🔍 상품 이름으로 찾는 SQL 명령 (부분 일치)
            # LIKE: "~처럼 생긴" 이라는 뜻 (모양이 비슷한 것 찾기)
            # %{product_name}%: 앞에도 뭐가 있고, 뒤에도 뭐가 있을 수 있지만,
            #                   중간에 이 이름이 있으면 된다는 뜻
            # 예) "스마트폰" 검색 → "스마트폰", "스마트폰2", "프리미엄스마트폰" 모두 찾음
            self.cursor.execute('SELECT * FROM Products WHERE productName LIKE ?', (f'%{product_name}%',))
            
            # 📋 조회한 모든 결과를 가져오기
            results = self.cursor.fetchall()
            
            # 결과 반환하기
            return results
        
        # 만약 조회가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []  # 빈 리스트 반환
    
    def select_by_price_range(self, min_price, max_price):
        """
        가격 범위로 상품 찾기
        
        설명: 마치 편의점에서 "1만원부터 5만원 사이의 상품 보여줘" 라고 물어보는 것처럼,
        특정 가격 범위에 해당하는 모든 상품을 찾습니다.
        
        매개변수 (파라미터):
            min_price: 최소 가격 (예: 100000)
            max_price: 최대 가격 (예: 500000)
        
        반환값:
            해당 가격 범위에 있는 모든 상품의 정보 리스트
            예: [(1, "스마트폰", 200000), (3, "태블릿", 300000), ...]
            없으면 빈 리스트 [] 반환
        """
        try:
            # 🔍 가격 범위로 찾는 SQL 명령
            # BETWEEN: "~와 ~ 사이에" 라는 뜻
            # productPrice BETWEEN ? AND ?: 상품 가격이 첫 번째 ?부터 두 번째 ?까지 사이에
            self.cursor.execute('''
                SELECT * FROM Products 
                WHERE productPrice BETWEEN ? AND ?
            ''', (min_price, max_price))
            # (min_price, max_price): 물음표(?) 자리에 들어갈 값
            #                          첫 번째 ? = min_price (최소 가격)
            #                          두 번째 ? = max_price (최대 가격)
            
            # 📋 조회한 모든 결과를 가져오기
            results = self.cursor.fetchall()
            
            # 결과 반환하기
            return results
        
        # 만약 조회가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 조회 실패: {e}")
            return []  # 빈 리스트 반환
    
    def update(self, product_id, product_name=None, product_price=None):
        """
        이미 있는 상품의 정보를 수정하기
        
        설명: 마치 편의점에서 가격표를 새로 붙이거나 상품 이름을 바꾸는 것처럼,
        데이터베이스에 저장된 상품 정보를 수정합니다.
        
        매개변수 (파라미터):
            product_id: 수정할 상품의 ID 번호 (필수)
            product_name: 새로운 상품 이름 (선택사항, None이면 변경 안 함)
            product_price: 새로운 상품 가격 (선택사항, None이면 변경 안 함)
        
        반환값:
            성공하면 True, 실패하면 False
        
        사용 예:
            update(1, "새로운 이름", 500000)  # 이름과 가격 둘 다 변경
            update(1, product_price=600000)   # 가격만 변경
            update(1, product_name="이름만")  # 이름만 변경
        """
        try:
            # 📝 상품 이름 수정하기 (이름이 지정되었을 때만)
            # if product_name is not None: product_name이 비어있지 않으면
            if product_name is not None:
                # UPDATE: "수정하다" 라는 뜻의 SQL 명령
                # Products SET productName = ?: Products 테이블에서 productName을 ?로 바꿔
                # WHERE productID = ?: productID가 ?인 행만 수정해
                self.cursor.execute('''
                    UPDATE Products SET productName = ?
                    WHERE productID = ?
                ''', (product_name, product_id))
            
            # 💰 상품 가격 수정하기 (가격이 지정되었을 때만)
            # if product_price is not None: product_price이 비어있지 않으면
            if product_price is not None:
                self.cursor.execute('''
                    UPDATE Products SET productPrice = ?
                    WHERE productID = ?
                ''', (product_price, product_id))
            
            # 💾 변경사항을 데이터베이스에 저장하기
            self.connection.commit()
            
            # ✅ 수정된 행이 있으면 True, 없으면 False 반환
            # rowcount: 영향을 받은 행의 개수
            return self.cursor.rowcount > 0
        
        # 만약 수정이 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 수정 실패: {e}")
            return False  # 실패를 나타내는 False 반환
    
    def delete(self, product_id):
        """
        특정 상품을 데이터베이스에서 삭제하기
        
        설명: 마치 편의점에서 "이 상품은 인기가 없어서 빼자" 라고 결정하고
        진열대에서 내려놓는 것처럼, 데이터베이스에서 상품을 삭제합니다.
        
        주의: 삭제되면 복구할 수 없습니다! (되돌릴 수 없음)
        
        매개변수 (파라미터):
            product_id: 삭제할 상품의 ID 번호
        
        반환값:
            성공하면 True, 실패하면 False
        """
        try:
            # 🗑️ 특정 상품을 삭제하는 SQL 명령
            # DELETE: "삭제하다" 라는 뜻의 SQL 명령
            # FROM Products: "Products 테이블에서"
            # WHERE productID = ?: "productID가 ?인 행을 삭제해"
            self.cursor.execute('DELETE FROM Products WHERE productID = ?', (product_id,))
            
            # 💾 변경사항을 데이터베이스에 저장하기
            self.connection.commit()
            
            # ✅ 삭제된 행이 있으면 True, 없으면 False 반환
            return self.cursor.rowcount > 0
        
        # 만약 삭제가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 데이터 삭제 실패: {e}")
            return False  # 실패를 나타내는 False 반환
    
    def delete_all(self):
        """
        모든 상품을 데이터베이스에서 삭제하기
        
        설명: 마치 편의점을 정리하면서 "모든 상품을 꺼내자" 라고 결정하고
        진열대를 완전히 비우는 것처럼, 테이블의 모든 데이터를 삭제합니다.
        
        주의: 모든 상품이 삭제됩니다! 되돌릴 수 없습니다!!
        
        반환값:
            성공하면 True, 실패하면 False
        """
        try:
            # 🗑️ 모든 상품을 삭제하는 SQL 명령
            # DELETE FROM Products: "Products 테이블의 모든 행을 삭제해"
            # WHERE 조건이 없으면 모든 행이 삭제됩니다
            self.cursor.execute('DELETE FROM Products')
            
            # 💾 변경사항을 데이터베이스에 저장하기
            self.connection.commit()
            
            # ✅ 몇 개를 삭제했는지 알려주기
            # rowcount: 영향을 받은 행의 개수
            print(f"✓ {self.cursor.rowcount}개 데이터 삭제 완료")
            
            return True  # 성공을 나타내는 True 반환
        
        # 만약 삭제가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 전체 데이터 삭제 실패: {e}")
            return False  # 실패를 나타내는 False 반환
    
    def get_count(self):
        """
        데이터베이스에 저장된 상품의 개수 세기
        
        설명: 마치 편의점 점장이 "우리 진열대에 상품이 몇 개 있지?" 라고
        세는 것처럼, 데이터베이스의 상품 개수를 셉니다.
        
        반환값:
            저장된 상품의 총 개수 (숫자)
            실패하면 0 반환
        """
        try:
            # 🔢 상품 개수를 세는 SQL 명령
            # COUNT(*): "모든 행의 개수를 세어"
            # *: "모든 것을" 라는 뜻 (모든 행을 센다는 의미)
            self.cursor.execute('SELECT COUNT(*) FROM Products')
            
            # 📋 결과를 하나만 가져오기 [0]: 첫 번째 항목을 선택
            # fetchone(): 한 개의 결과를 튜플 형태로 가져옴
            # (10,) 이런 식으로 나오는데, [0]을 붙여서 숫자 10만 추출
            count = self.cursor.fetchone()[0]
            
            # 개수 반환하기
            return count
        
        # 만약 개수 세기가 실패하면 이 부분이 실행됩니다
        except sqlite3.Error as e:
            print(f"✗ 개수 조회 실패: {e}")
            return 0  # 0 반환 (개수를 셀 수 없음)
    
    def close(self):
        """
        데이터베이스 연결 종료하기
        
        설명: 마치 편의점 문을 닫고 "오늘은 여기까지!" 라고 선언하는 것처럼,
        데이터베이스와의 연결을 끊습니다.
        
        중요: 모든 작업이 끝나면 반드시 이 함수를 호출해야 합니다!
        프로그램을 종료하기 전에 항상 close()를 호출하세요.
        """
        # 🔌 연결이 있으면 종료하기
        if self.connection:
            # close(): 연결 종료하기 (전화를 끊는 것처럼)
            self.connection.close()
            
            # 종료 메시지 출력
            print("✓ 데이터베이스 연결 종료")


# ========== 🎲 샘플 데이터 만드는 함수 ==========
def generate_sample_data(count=10000):
    """
    테스트용 샘플 상품 데이터 만들기
    
    설명: 이 함수는 데이터베이스를 테스트하기 위해 가짜 상품 데이터를 만듭니다.
    마치 "1만개의 상품을 상상해서 종이에 적어두기" 같은 것입니다.
    
    매개변수 (파라미터):
        count: 만들 상품의 개수 (기본값: 10000개)
              예: count=100 → 100개의 샘플 데이터 생성
    
    반환값:
        (상품이름, 상품가격) 쌍으로 이루어진 리스트
        예: [("스마트폰 1", 250000), ("노트북 2", 850000), ...]
    """
    # 📦 상품 이름의 종류 정하기
    # 이 리스트 중에서 무작위로 선택해서 상품을 만듭니다
    product_names = [
        "스마트폰", "노트북", "태블릿", "이어폰", "충전기",
        "마우스", "키보드", "모니터", "프린터", "공기청정기",
        "선풍기", "가습기", "냉장고", "전자레인지", "세탁기",
        "건조기", "식기세척기", "에어컨", "히터", "가스렌지",
        "오디오", "카메라", "드론", "게임기", "스피커"
    ]
    
    # 🎁 빈 리스트 만들기 (샘플 상품들을 넣을 상자)
    products = []
    
    # 🔄 반복문: count개(10000개)만큼 반복하기
    # for i in range(count): i가 0부터 9999까지 증가하면서 반복
    for i in range(count):
        # 🎲 상품 이름 만들기
        # random.choice(product_names): product_names 리스트에서 무작위로 하나 선택
        # + f" {i+1}": 선택한 이름 뒤에 번호를 붙이기 (예: "스마트폰 1", "노트북 2")
        product_name = random.choice(product_names) + f" {i+1}"
        
        # 💰 상품 가격 만들기
        # random.randint(10000, 500000): 10,000원부터 500,000원 사이의 무작위 숫자
        # 마치 주사위를 던져서 나온 숫자처럼 매번 다른 숫자가 나옵니다
        product_price = random.randint(10000, 500000)
        
        # 📝 만든 상품을 리스트에 추가하기
        # (product_name, product_price): (이름, 가격) 형태의 쌍으로 만들기
        products.append((product_name, product_price))
    
    # ✨ 만들어진 상품 리스트 반환하기
    return products


# ========== 💻 프로그램 실행 부분 ==========
# if __name__ == "__main__": 
#   "이 파일을 직접 실행할 때만 이 코드를 실행해"라는 뜻
#   다른 파일에서 import될 때는 이 코드가 실행되지 않습니다
if __name__ == "__main__":
    # ========== 1️⃣ ProductManager 객체 만들기 ==========
    # ProductManager("MyProduct.db")를 실행하면:
    # - 자동으로 MyProduct.db 파일이 생성됩니다
    # - 자동으로 Products 테이블이 만들어집니다
    # - 데이터베이스와 연결됩니다
    pm = ProductManager("MyProduct.db")
    
    # ========== 2️⃣ 데이터베이스 초기화 (청소하기) ==========
    # 만약 이전에 저장된 데이터가 있으면 모두 지우기
    # 새로운 시작을 위해 테이블을 깨끗이 비웁니다 (리셋!)
    print("\n" + "="*50)
    print("기존 데이터 초기화")
    print("="*50)
    # pm.delete_all(): 모든 상품 데이터 삭제하기
    pm.delete_all()
    
    # ========== 3️⃣ 샘플 데이터 1만개 생성 및 삽입 ==========
    # "가짜 상품 10,000개를 만들고 데이터베이스에 넣기"
    print("\n" + "="*50)
    print("샘플 데이터 1만개 생성 및 삽입")
    print("="*50)
    
    # ⏱️ 시작 시간 기록하기 (얼마나 빨리 완료되는지 재기 위해)
    start_time = datetime.now()
    
    # 🎲 샘플 데이터 10,000개 만들기
    sample_data = generate_sample_data(10000)
    
    # 📤 만든 데이터를 데이터베이스에 한 번에 넣기
    pm.insert_many(sample_data)
    
    # ⏱️ 끝난 시간 기록하기
    end_time = datetime.now()
    
    # ⏰ 소요 시간 계산하고 표시하기
    # .total_seconds(): 시간차이를 초 단위로 변환
    # :.2f: 소수점 이하 2자리까지만 표시
    print(f"소요 시간: {(end_time - start_time).total_seconds():.2f}초")
    
    # ========== 4️⃣ 데이터 조회 테스트 (SELECT - 읽기) ==========
    # 이제 만든 데이터를 여러 방법으로 검색해보기
    print("\n" + "="*50)
    print("데이터 조회 테스트")
    print("="*50)
    
    # 🔢 전체 상품 개수 세기
    # "우리 데이터베이스에 총 몇 개의 상품이 있어?"
    total_count = pm.get_count()
    print(f"\n[전체 제품 개수]: {total_count}개")
    
    # 📋 모든 상품 조회 (첫 5개만 보여주기)
    # pm.select_all()[:5]: 모든 상품을 조회하되, 처음 5개만 선택
    # [:5]: "0번부터 4번까지 (5개)" 라는 뜻
    print("\n[전체 제품 조회 - 처음 5개]:")
    all_products = pm.select_all()[:5]  # 상품 리스트에서 처음 5개만 선택
    
    # 🔄 선택한 5개 상품을 하나씩 출력하기
    # for product in all_products: 각 상품마다 반복하면서
    for product in all_products:
        # product[0]: 상품ID, product[1]: 상품이름, product[2]: 상품가격
        # {:,} 형식: 숫자에 쉼표를 붙여서 보기 좋게 표시
        # 예) 250000 → 250,000
        print(f"  ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 🔍 특정 ID로 조회 (100번 상품은 뭐지?)
    # "우리 데이터베이스에서 ID가 100인 상품을 찾아줘"
    print("\n[ID 100번 제품 조회]:")
    product = pm.select_by_id(100)
    
    # if product: 만약 상품을 찾았으면
    if product:
        print(f"  ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 🔍 상품 이름으로 조회 (스마트폰이라는 이름을 가진 상품 찾기)
    # "스마트폰"이라는 이름을 포함하는 모든 상품을 찾기
    # 예) "스마트폰", "스마트폰2", "프리미엄스마트폰" 모두 찾음
    print("\n[스마트폰 제품 조회]:")
    products = pm.select_by_name("스마트폰")[:3]  # 찾은 것 중 처음 3개만 선택
    
    # 🔄 선택한 3개 상품을 하나씩 출력하기
    for product in products:
        print(f"  ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 🔍 가격 범위로 조회 (100,000원~150,000원 사이의 상품)
    # "100,000원부터 150,000원 사이의 상품을 찾아줘"
    print("\n[가격 100,000 ~ 150,000원 범위 제품 조회 - 처음 5개]:")
    products = pm.select_by_price_range(100000, 150000)[:5]  # 찾은 것 중 처음 5개만
    
    # 🔄 선택한 5개 상품을 하나씩 출력하기
    for product in products:
        print(f"  ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # ========== 5️⃣ 데이터 수정 테스트 (UPDATE - 수정) ==========
    # "ID 1번 상품의 이름과 가격을 바꾸기"
    print("\n" + "="*50)
    print("데이터 수정 테스트")
    print("="*50)
    
    # 📝 수정하기 전에 먼저 확인해보기
    print("\n[ID 1번 제품 수정 전]:")
    product = pm.select_by_id(1)
    print(f"  이름: {product[1]}, 가격: {product[2]:,}원")
    
    # ✏️ ID 1번 상품의 정보 수정하기
    # "이름을 '프리미엄 스마트폰 A'로 바꾸고, 가격을 899,000원으로 바꿔"
    pm.update(1, "프리미엄 스마트폰 A", 899000)
    
    # 📝 수정한 후 다시 확인해보기
    print("\n[ID 1번 제품 수정 후]:")
    product = pm.select_by_id(1)
    print(f"  이름: {product[1]}, 가격: {product[2]:,}원")
    
    # ========== 6️⃣ 데이터 삭제 테스트 (DELETE - 삭제) ==========
    # "ID 1, 2, 3번 상품을 삭제하기"
    print("\n" + "="*50)
    print("데이터 삭제 테스트")
    print("="*50)
    
    # 🔢 삭제하기 전에 현재 상품 개수 세기
    print(f"\n[삭제 전 개수]: {pm.get_count()}개")
    
    # 🗑️ ID 1, 2, 3번 상품을 하나씩 삭제하기
    pm.delete(1)
    pm.delete(2)
    pm.delete(3)
    
    # 🔢 삭제 후 남은 상품 개수 세기
    print(f"[ID 1, 2, 3 삭제 후 개수]: {pm.get_count()}개")
    
    # ========== 7️⃣ 데이터베이스 연결 종료 ==========
    # "프로그램을 종료하기 전에 데이터베이스 연결을 끊기"
    # 마치 편의점 문을 닫고 가는 것처럼!
    print("\n" + "="*50)
    # pm.close(): 데이터베이스 연결 종료하기 (중요!)
    pm.close()
    print("="*50)
    # 프로그램 완료!
