#정규표현식
import re

result = re.search("[0-9]*th", "35th")
print(result)
print(result.group())

# result = re.match("[0-9]*th", "35th")
# print(result)
# print(result.group())

#연도 찾기
result = re.search("\d{4}", "올해는 2024년입니다.")
print(result.group())

#우편번호찾기
result = re.search("\d{5}", "우리동네 우편번호는 12345입니다.")
print(result.group())

#단어
result = re.search("apple", "this is an Apple".lower())
print(result.group())