
def precision(a, b):
    p = a / (a+b)
    return p

def relevend(a,c):
    relv = a / (a+c)
    return relv

def f_measures(p,r):
    f = 2 * ((p*r)/(p+r))
    return f

def accuracy(a,b,c,d):
    acc =  (a + d) / (a+b+c+d)
    return acc

a = 12
b = 12  # 10 , 14 , 8
c = 1
d = 58  # 42 , 58 , 32
p = precision(a,b)
print("Precision: ",p)
r = relevend(a,c)
print("Relevand: ",r)
ac = accuracy(a,b,c,d)
print("accuracy :", ac)
f = f_measures(p,r)
print("F -Measures: ",f)