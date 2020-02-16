count = 0
mydict = {1:0,2:0,3:0}
length  = len(mydict)
for i in range(1,length+1):
    if mydict[i] != 0:
        count += 1
        break
count1 = count


if count1 != 0:
    print("It worked")
else:
    print("It didn't work")





