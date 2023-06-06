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
