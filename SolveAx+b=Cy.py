PrimeMax=1000
import math
from sympy import *

def GCD(a,b):
    return math.gcd(a,b)

def Prime(n):
    if isprime(n):
        return 1
    else:
        return 0

def AnOverM(a,M):
    a0=a
    n=1
    f=0
    while a<M:
        a*=a0
        n+=1
    if a==M: f=1
    return n,f

def PowerMod(a,n,M):
    if n==0: return 1
    a0=a
    for i in range(1,n):
        a*=a0
        while a>=M: a-=M
    return a

def CycleAndPosition(a,M,N):
    n=1
    s=a
    k=-1
    while s!=1:
        s*=a
        while s>M:
            s-=M
        n+=1
        if(s==N):
            k=n
    if a%M==N : k=1
    return n,k
    
def Exhaust(a,b,c,x0,y0):
    print("因此x<=%d或y<=%d"%(x0,y0))
    if x0<1 and y0<1: 
        print("因此方程%d^x+%d=%d^y没有正整数解"%(a,b,c))
        return
    flag=0
    S=set()
    if x0>=1:
        for i in range(1,x0+1):
            K=pow(a,i)+b
            y,f=AnOverM(c,K)
            if f==0: 
                continue
            else:
                S.add((i,y))
                flag=1
    if y0>=1:
        for i in range(1,y0+1):
            K=pow(c,i)-b
            if K<1: continue
            x,f=AnOverM(a,K)
            if f==0:
                continue
            else:
                S.add((x,i))
    if flag==0:
        print("经过穷举发现，原方程无正整数解！")
    else:
        print("经过穷举发现，原方程的正整数解有：")
        for t in S:
            print("(x,y)=(%d,%d)"%(t[0],t[1]))
    return

def Solve1(a,b,c):
    G=GCD(a,c)
    N,flag=AnOverM(G,b)
    if flag==1: N+=1
    M=pow(G,N)
    print("反设x>=%d且y>=%d"%(N,N))
    print("将方程两边同时对%d取模，得%d≡0 mod %d"%(M,b,M))
    print("但这是不可能的")
    Exhaust(a,b,c,N-1,N-1)
    return
    
def Solve2(a,b,c):
    x0=int(input("请输入归谬假设x>=x0中x0的值："))
    y0=int(input("请输入归谬假设y>=y0中y0的值："))
    print("反设x>=%d且y>=%d"%(x0,y0))
    A=pow(a,x0)
    C=pow(c,y0)
    print("将方程两边同时对%d^%d=%d取模，得%d^x≡%d≡%d mod %d"%(c,y0,C,a,0-b,(0-b)%C,C))
    Mx,n=CycleAndPosition(a,C,(0-b)%C)
    if n==-1:
        print("但这是不可能的")
        Exhaust(a,b,c,x0-1,y0-1)
    else:
        print("因此x≡%d mod %d"%(n%Mx,Mx))
    print("将方程两边同时对%d^%d=%d取模，得%d^y≡%d≡%d mod %d"%(a,x0,A,c,b,b%A,A))
    My,m=CycleAndPosition(c,A,b%A)
    if m==-1:
        print("但这是不可能的")
        Exhaust(a,b,c,x0-1,y0-1)
    else:
        print("因此y≡%d mod %d"%(m%My,My))
    while true:
        str=input("请输入归谬模式（Front/Back）:")
        if str=="Front":
            FrontSolve2(a,b,c,x0,y0,n,Mx,m,My)
            break
        elif str=="Back":
            BackSolve2(a,b,c,x0,y0,n,Mx,m,My)
            break
        else:
            print("不存在此归谬模式，请重新输入！")
    return

def FrontSolve2(a,b,c,x0,y0,n,Mx,m,My):
    N=-1
    P=-1
    for i in range(1,PrimeMax):
        P=Mx*i+1
        if Prime(P)==0:
            continue
        elif a%P==0 or c%P==0:
            continue
        else:
            if CycleAndPosition(a,P,1)[0]%Mx!=0:
                continue
            else:
                N=CycleAndPosition(a,P,1)[0]//Mx
                break
    if N==-1:
        print("没有找到合适素数！")
        return
    print("关于%d^x的合适的模数是%d"%(a,P))
    cyModP=set()
    print("%d^x mod %d的可能取值包括："%(a,P))
    for i in range(0,N):
        t=PowerMod(a,n+i*Mx,P)
        print(t)
        cyModP.add((t+b)%P)
    print("这意味着%d^y mod %d的可能取值包括："%(c,P))
    flag=0
    for i in cyModP:
        print(i)
        if(CycleAndPosition(c,P,i)[1]!=-1): flag=1
    if flag==0:
        print("但这是不可能的")
        Exhaust(a,b,c,x0-1,y0-1)
        return
    print("因此以下条件必成立其一：")
    for i in cyModP:
        if(CycleAndPosition(c,P,i)[1]!=-1):
            xx=CycleAndPosition(c,P,i)[1]
            yy=CycleAndPosition(c,P,i)[0]
            print("y≡%d mod %d"%(xx,yy))
    Myy=CycleAndPosition(c,P,1)[0]
    if GCD(Myy,My)==1:
        print("未能成功归谬，请尝试增大x0或y0的值！")
        return
    else:
        print("在以上条件中，")
        flag=0
        MY=GCD(Myy,My)
        for i in cyModP:
            if(CycleAndPosition(c,P,i)[1]!=-1):
                xx=CycleAndPosition(c,P,i)[1]
                if xx%MY==m%MY:
                    flag=1
                    print("y≡%d mod %d"%(xx,CycleAndPosition(c,P,i)[0]))
        if flag==0:
            print("没有条件和y≡%d mod %d兼容，推出矛盾！"%(m,My))
            Exhaust(a,b,c,x0-1,y0-1)
        else:
            print("和条件y≡%d mod %d兼容"%(m,My))
            print("未能成功归谬，请尝试增大x0或y0的值！")
    return

def BackSolve2(a,b,c,x0,y0,n,Mx,m,My):
    N=-1
    P=-1
    for i in range(1,PrimeMax):
        P=My*i+1
        if Prime(P)==0:
            continue
        elif a%P==0 or c%P==0:
            continue
        else:
            if CycleAndPosition(c,P,1)[0]%My!=0:
                continue
            else:
                N=CycleAndPosition(c,P,1)[0]//My
                break
    if N==-1:
        print("没有找到合适素数！")
        return
    print("关于%d^y的合适的模数是%d"%(c,P))
    axModP=set()
    print("%d^y mod %d的可能取值包括："%(c,P))
    for i in range(0,N):
        t=PowerMod(c,n+i*My,P)
        print(t)
        axModP.add((t-b)%P)
    print("这意味着%d^x mod %d的可能取值包括："%(a,P))
    flag=0
    for i in axModP:
        print(i)
        if(CycleAndPosition(a,P,i)[1]!=-1): flag=1
    if flag==0:
        print("但这是不可能的")
        Exhaust(a,b,c,x0-1,y0-1)
        return
    print("因此以下条件必成立其一：")
    for i in axModP:
        if(CycleAndPosition(a,P,i)[1]!=-1):
            xx=CycleAndPosition(a,P,i)[1]
            yy=CycleAndPosition(a,P,i)[0]
            print("x≡%d mod %d"%(xx,yy))
    Mxx=CycleAndPosition(a,P,1)[0]
    if GCD(Mxx,Mx)==1:
        print("未能成功归谬，请尝试增大x0或y0的值！")
        return
    else:
        print("在以上条件中，")
        flag=0
        MX=GCD(Mxx,Mx)
        for i in axModP:
            if(CycleAndPosition(a,P,i)[1]!=-1):
                xx=CycleAndPosition(a,P,i)[1]
                if xx%MX==n%MX:
                    flag=1
                    print("x≡%d mod %d"%(xx,CycleAndPosition(a,P,i)[0]))
        if flag==0:
            print("没有条件和x≡%d mod %d兼容，推出矛盾！"%(n,Mx))
            Exhaust(a,b,c,x0-1,y0-1)
        else:
            print("和条件x≡%d mod %d兼容"%(n,Mx))
            print("未能成功归谬，请尝试增大x0或y0的值！")
    return

def Solve(a,b,c):
    print("对于方程%d^x+%d=%d^y"%(a,b,c))
    if GCD(a,c)>1:
        print("%d和%d的最大公因数为%d，大于1"%(a,c,GCD(a,c)))
        Solve1(a,b,c)
    else:
        Solve2(a,b,c)
    return

print("此程序严格求解关于正整数x和y的不定方程a^x+b=c^y，其中a,b,c都是给定的正整数且a和c都大于1")
a=int(input("请键入a的值："))
b=int(input("请键入b的值："))
c=int(input("请键入c的值："))
Solve(a,b,c)
while input("键入Again再次求解，键入其他任意字符退出程序：")=="Again":
    a=int(input("请键入a的值："))
    b=int(input("请键入b的值："))
    c=int(input("请键入c的值："))
    Solve(a,b,c)

