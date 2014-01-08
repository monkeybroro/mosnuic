def add_bin(a,b):
    la=len(a)
    lb=len(b)
    if la>lb:
        b='0'*(la-lb)+b
    else:
        a='0'*(lb-la)+a
        
    c=[]
    for i in range(0,len(a)):
        c.append(str(int(a[i])+int(b[i])))

    c=map(int,c)
    carry=0
    for i in range(len(c)-1,-1,-1):
        c[i]=c[i]+carry
        if c[i]>=2:
            c[i]=c[i]%2
            carry=1
    if carry==1:
        c.insert(0,1)

    c=map(str,c)
    x=''
    for i in c:
        x+=i
    return x
    
