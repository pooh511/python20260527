# db 연습
import sqlite3

# 연결객체
con = sqlite3.connect(":memory:")  # 메모리상에서만 존재하는 데이터베이스


# 커서객체
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS" +
            " phonebook(name TEXT, phone TEXT)")

#입력
cur.execute("INSERT INTO phonebook VALUES('John Doe','010-1234-5678')")
#검색
cur.execute("SELECT * FROM phonebook")
for row in cur.execute("SELECT * FROM phonebook"):
    print(row)