import sys

def floattobin(f):
    if f==0:
        return '00000000'
    temp=str(f).split('.')
    dec=bin(int(temp[0]))[2:]
    floating=float('0.'+temp[1])
    binfloat=""
    for i in range(5):
        floating*=2
        if floating>=2:
            floating=float('0.'+str(floating).split('.')[1])
        binfloat=binfloat+str(int(floating))
    exponent=len(dec)-1+3
    mantissa=dec[1:]+binfloat
    ans=(bin(exponent)[2:]+mantissa).rstrip('0')
    numbits=len(ans)
    if numbits>8:
        return 'overflow'
    elif numbits<8:
        return ans+('0'*(8-len(ans)))
    else:
        return ans


def bintofloat(b):
    if b=='00000000':
        return 0.0
    exponent=b[:3]
    mantissa=b[3:]
    power=int(exponent,2)-3
    floating=0
    for i in range(5):
        floating=floating+int(mantissa[i])(2*(-(i+1)))
    ans=(1+floating)(2*(power))
    return ans

def movImm(regval,reg,temp):
    regval[reg]=format(temp,"016b")

def movReg(regval,reg1,reg2):
    regval[reg1]=regval[reg2]

def load(regval,memory,reg,address):
    regval[reg]=memory[address]

def store(regval,memory,reg,address):
    memory[address]=regval[reg]

def xor(regval,reg1,reg2,reg3):
    regval[reg1]=format(int(regval[reg2][9:],2) ^ int(regval[reg3][9:],2),"016b")

def Or(regval,reg1,reg2,reg3):
    regval[reg1]=format(int(regval[reg2][9:],2) | int(regval[reg3][9:],2),"016b")

def And(regval,reg1,reg2,reg3):
    regval[reg1]=format(int(regval[reg2][9:],2) & int(regval[reg3][9:],2),"016b")

def invert(regval,reg1,reg2):
    Not=""
    for i in range(9,16):
        if regval[reg2][i]=="0":
            Not+="1"
        elif regval[reg2][i]=="1":
            Not+="0"
    regval[reg1]=format(int(Not,2),"016b")

def rshift(regval,reg1,num):
    regval[reg1]=format(int(regval[reg1][9:],2)>>int(num),"016b")

def lshift(regval,reg1,num):
    regval[reg1]=format(int(regval[reg1][9:],2)<<int(num),"016b")

def multiply(regval,reg1,reg2,reg3):
    prod=int(regval[reg2][9:],2)*int(regval[reg3][9:],2)
    if prod>127:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
        return True
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(prod,"016b")
        return False

def divide(regval,reg1,reg2):
    if regval[reg2]=="0000000000000000":
        regval["FLAGS"]="0000000000001000"
        regval["R0"]="0000000000000000"
        regval["R1"]="0000000000000000"
        return True
    else:
        regval["R0"]=format(int(regval[reg1][9:],2)//int(regval[reg2][9:],2),"016b")
        regval["R1"]=format(int(regval[reg1][9:],2)%int(regval[reg2][9:],2),"016b")
        regval["FLAGS"]="0000000000000000"
        return False

def add(regval, reg1, reg2, reg3):
    sum=int(regval[reg2][9:],2)+int(regval[reg3][9:],2)
    if sum>127:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
        return True
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(sum,"016b")
        return False

def sub(regval, reg1, reg2, reg3):
    if int(regval[reg3],2)>int(regval[reg2],2):
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
        return True
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(int(regval[reg2],2)-int(regval[reg3],2),"016b")
        return False

def cmp(regval,reg1,reg2):
    if (regval[reg1]<regval[reg2]):
        regval["FLAGS"]="0000000000000100"
    elif (regval[reg1]>regval[reg2]):
        regval["FLAGS"]="0000000000000010"
    else:
        regval["FLAGS"]="0000000000000001"

def jlt(program_counter,regval,address):
    if regval["FLAGS"][-3]=="1":
        program_counter=address
    return program_counter

def jgt(program_counter,regval,address):
    if regval["FLAGS"][-2]=="1":
        program_counter=address
    return program_counter

def je(program_counter,regval,address):
    if regval["FLAGS"][-1]=="1":
        program_counter=address
    return program_counter

def jmp(address):
    program_counter=address
    return program_counter    
