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

def not_chip(a):
    return nand(a, a)

def halfadder(a, b):
    suma = xor_chip(a, b)
    acarreo = and_chip(a, b)
    return {"Carry_H": acarreo, "Sum_H": suma}

def fulladder(a, b, c):
    out1 = halfadder(a, b)
    suma = halfadder(out1["Sum_H"], c)
    acarreo = or_chip(out1["Carry_H"], suma["Carry_H"])
    return {"Carry_F": acarreo, "Sum_F": suma["Sum_H"]}

def add16(a, b):
    output = [0] * 16
    acarreo = 0
    for i in range(15, -1, -1):
        resultado = fulladder(a[i], b[i], acarreo)
        output[i] = resultado["Sum_F"]
        acarreo = resultado["Carry_F"]
    if acarreo == 1:
        output.insert(0, 1)
    return output

def inc16(a):
    b = [0] * 15 + [1]
    return add16(a, b)

def ALU(x, y, zx, nx, zy, ny, f, no):
    if zx:
        x = [0] * 16
    if nx:
        x = [not_chip(bit) for bit in x]
    if zy:
        y = [0] * 16
    if ny:
        y = [not_chip(bit) for bit in y]
    if f:
        out = add16(x, y)
    else:
        out = [and_chip(x[i], y[i]) for i in range(16)]
    if no:
        out = [not_chip(bit) for bit in out]
    return out

def generate_outputs():
    operations = ["0", "1", "-1", "x", "y", "!x", "!y", "-x", "-y", "x+1", "y+1", "x-1", "y-1", "x+y", "x-y", "y-x", "x&y", "x|y"]
    x = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
    y = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
    results = {}
    results["0"] = [0] * 16
    results["1"] = [1] * 16
    results["-1"] = [1] * 16
    results["x"] = x
    results["y"] = y
    results["!x"] = [not_chip(bit) for bit in x]
    results["!y"] = [not_chip(bit) for bit in y]
    results["-x"] = add16([not_chip(bit) for bit in x], [0]*15 + [1])
    results["-y"] = add16([not_chip(bit) for bit in y], [0]*15 + [1])
    results["x+1"] = inc16(x)
    results["y+1"] = inc16(y)
    results["x-1"] = add16(x, [1]*15 + [1])
    results["y-1"] = add16(y, [1]*15 + [1])
    results["x+y"] = add16(x, y)
    results["x-y"] = add16(x, add16([not_chip(bit) for bit in y], [0]*15 + [1]))
    results["y-x"] = add16(y, add16([not_chip(bit) for bit in x], [0]*15 + [1]))
    results["x&y"] = [and_chip(x[i], y[i]) for i in range(16)]
    results["x|y"] = [or_chip(x[i], y[i]) for i in range(16)]
    
    for op in operations:
        print(f"{op}: {results[op]}")

def main():
    generate_outputs()

if __name__ == "__main__":
    main()

