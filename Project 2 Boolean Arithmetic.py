def nand(a, b):
    return 0 if (a == 1 and b == 1) else 1

def xor_chip(a, b):
    n1 = nand(a, b)
    n2 = nand(a, n1)
    n3 = nand(n1, b)
    out = nand(n2, n3)
    return out

def and_chip(a, b):
    out = nand(nand(a, b), nand(a, b))
    return out

def or_chip(a, b):
    out = nand(nand(a, a), nand(b, b))
    return out

#HalfAdder
def halfadder(a,b):
    suma = xor_chip(a,b)
    acarreo = and_chip(a,b)
    outputs = {"Carry_H":acarreo, "Sum_H":suma}
    return outputs

"""print("HalfAdder")
prueba_ = halfadder(0,0)
prueba_1 = halfadder(0,1)
prueba_2 = halfadder(1,0)
prueba_3 = halfadder(1,1)
print(prueba_)
print(prueba_1)
print(prueba_2)
print(prueba_3)"""

#FullAdder
def fulladder(a,b,c):
    out1 = halfadder(a,b)
    suma = halfadder(out1["Sum_H"],c)
    acarreo = or_chip(out1["Carry_H"],suma["Carry_H"])
    outputs = {"Carry_F":acarreo, "Sum_F":suma["Sum_H"]}
    return outputs

"""print("FullfAdder")
prueba = fulladder(0,0,0)
prueba1 = fulladder(0,0,1)
prueba2 = fulladder(0,1,0)
prueba3 = fulladder(0,1,1)
prueba4 = fulladder(1,0,0)
prueba5 = fulladder(1,0,1)
prueba6 = fulladder(1,1,0)
prueba7 = fulladder(1,1,1)
print(prueba)
print(prueba1)
print(prueba2)
print(prueba3)
print(prueba4)
print(prueba5)
print(prueba6)
print(prueba7)"""

#Add16
def add16(a = [0,1,0,0,0,0,0,1,1,1,0,1,0,1,0,1], 
          b = [1,1,1,1,1,1,1,1,1,0,0,0,0,1,0,1]):
    output=[0]*16
    acarreo = 0
    for i in range(15,-1,-1):
        resultado = fulladder(a[i],b[i],acarreo)
        output[i]=resultado["Sum_F"]
        acarreo = resultado["Carry_F"]
    if acarreo == 1:
        output.insert(0,1)    
    return output

#print(add16())

#Inc16
def inc16(a=[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0]):
    b = [0]*15+[1]
    output = add16(a,b)
    return output

#print(inc16())

#ALU

