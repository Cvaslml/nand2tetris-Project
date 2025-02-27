def nand(a, b):
    return 0 if (a == 1 and b == 1) else 1

# Definición de puertas básicas
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

def not_chip(a):
    return nand(a, a)

# Half Adder
def halfadder(a, b):
    suma = xor_chip(a, b)
    acarreo = and_chip(a, b)
    return {"Carry_H": acarreo, "Sum_H": suma}

# Full Adder
def fulladder(a, b, c):
    out1 = halfadder(a, b)
    suma = halfadder(out1["Sum_H"], c)
    acarreo = or_chip(out1["Carry_H"], suma["Carry_H"])
    return {"Carry_F": acarreo, "Sum_F": suma["Sum_H"]}

# ALU basada en la tabla de verdad
def alu(x, y, zx, nx, zy, ny, f, no):
    if zx:  # Si zx es 1, x = 0
        x = 0
    if nx:  # Si nx es 1, x = !x
        x = not_chip(x)
    if zy:  # Si zy es 1, y = 0
        y = 0
    if ny:  # Si ny es 1, y = !y
        y = not_chip(y)
    
    if f:
        out = fulladder(x, y, 0)["Sum_F"]  # Suma si f=1
    else:
        out = and_chip(x, y)  # AND si f=0
    
    if no:
        out = not_chip(out)  # Negación de la salida si no=1
    
    return out

# Prueba de la ALU con una configuración específica
print(alu(1, 1, 0, 0, 0, 0, 1, 0))  # Debería hacer x + y

