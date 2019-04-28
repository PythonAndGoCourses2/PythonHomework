ss=[]
s=[0,",",3,2,',',3,4,6]
s=[2,',',1]
#s=[1,2,3,4]
i=len(s)-2
ss.append(s[-1])
print(*s,sep=' ')
print(i,s[i])
while s[i] == ',':
	ss.append(s[i-1])
	i=i-2
	print(i, s[i])
print('out',i)
print(*s[i+1:],sep=' ')
ss.reverse()
print(ss)
