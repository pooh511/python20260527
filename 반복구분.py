#repeat phase-while

value =5
while value >0 :
    print(value)
    value -=1

#2) for in
print("for~in loop")
for i in [1,2,3]:
    print(i)

#dictionary
d = {"name":"Donald J.Trump","age":30,"address":"Washington DC"}

for item in d.items():
    print(item)



print("----range function-----")
print(list(range(2000,2017)))
print(list(range(1,32)))
print(list(range(1,11,2)))

for i in range(5):
    print(i)

print("list comprehension")
lst= [1,2,3,4,5,6,7,8,9,10]
print([i**2 for i in lst if 1>5])
tp = ("apple","kiwi")
print([len(i) for i in tp])
d= {100: "apple", 200: "kiwi"}
print( [v.upper() for v in d.values()])


print("Filtering")
lst =[10,25,30]
itemL = filter(None, lst)
for item in itemL:
    print(item)

print("filtering2")
def getBiggerThan20(i):
    return i>20
lst = [10,25,30]
itemL = filter(getBiggerThan20, lst)
for item in itemL:
    print(item)
