lst = [1,2,3,4,5,6,7,8,9]
sum = 10
newlist=[]
for i in lst:
    if([i]+[i+1]==sum):
        newlist= newlist.append(i)
print(newlist)


