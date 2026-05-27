# db 연습2
import sqlite3

# 연결객체
con = sqlite3.connect("c:\\work\\sample.db")  # 메모리상에서만 존재하는 데이터베이스


# 커서객체
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS" +
            " phonebook(name TEXT, phone TEXT)")

#입력
datalist =([('John Doe', '010-1234-5678'),('Jane Smith', '010-9876-5432')])

cur.executemany("INSERT INTO phonebook VALUES(?, ?)", datalist)
    #검색
cur.execute("SELECT * FROM phonebook")
for row in cur.execute("SELECT * FROM phonebook"):
    print(row)


#commit
    con.commit()
    con.close()
