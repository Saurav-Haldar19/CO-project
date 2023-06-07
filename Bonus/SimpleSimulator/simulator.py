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
        floating=floating+int(mantissa[i])*(2**(-(i+1)))
    ans=(1+floating)*(2**(power))
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

def addf(regval,reg1,reg2,reg3):
    sum=bintofloat(regval[reg2][8:])+bintofloat(regval[reg3][8:])
    binsum=floattobin(sum)
    if binsum=='overflow':
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
        return True
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=(8*'0')+binsum
        return False
    
def subf(regval,reg1,reg2,reg3):
    dif=bintofloat(regval[reg2][8:])-bintofloat(regval[reg3][8:])
    if dif<0.25 and dif!=0:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
        return True
    else:
        bindif=floattobin(sum)
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=(8*'0')+bindif
        return False
    
def movf(regval,reg1,imm):
    regval[reg1]=(8*'0')+imm

def Nor(regval,reg1,reg2,reg3):
    Or(regval,reg1,reg2,reg3)
    invert(regval,reg1,reg1)

def Nand(regval,reg1,reg2,reg3):
    And(regval,reg1,reg2,reg3)
    invert(regval,reg1,reg1)

def Xnor(regval,reg1,reg2,reg3):
    xor(regval,reg1,reg2,reg3)
    invert(regval,reg1,reg1)

def Max(regval,reg1,reg2):
    num1=int(regval[reg1][9:],2)
    num2=int(regval[reg2][9:],2)
    if num1>num2:
        regval[reg1]=format(num1,"016b")
    else:
        regval[reg1]=format(num2,"016b")

def Min(regval,reg1,reg2):
    num1=int(regval[reg1][9:],2)
    num2=int(regval[reg2][9:],2)
    if num1<num2:
        regval[reg1]=format(num1,"016b")
    else:
        regval[reg1]=format(num2,"016b")

op={'00000': 'add', '00001': 'sub', '00010': 'movi', '00011': 'mov', '00100': 'ld', '00101': 'st', '00110': 'mul', '00111': 'div', '01000': 'rs', '01001': 'ls', '01010': 'xor', '01011': 'or', '01100': 'and', '01101': 'not', '01110': 'cmp', '01111': 'jmp', '11100': 'jlt', '11101': 'jgt', '11111': 'je', '11010': 'hlt','10000':'addf','10001':'subf','10010':'movf','10011':'nor','10100':'nand','10101':'xnor','10110':'max','10111':'min'}
regval={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
reg={'000': 'R0', '001': 'R1', '010': 'R2', '011': 'R3', '100': 'R4', '101': 'R5', '110': 'R6', '111': 'FLAGS'}
memory=[]
for i in range(128):
    memory.append("0000000000000000")
Input=sys.stdin
instructions=[]
for i in Input:
    instructions.append(i.strip())
typeA=["add","sub","mul","xor","or","and","addf","subf","nor","nand","xnor"]
typeB=["movi","rs","ls","movf"]
typeC=["mov","div","not","cmp","max","min"]
typeD=["ld","st"]
typeE=["jmp","jlt","jgt","je"]
for i in range(len(instructions)):
    instructions[i]=instructions[i].strip()
    memory[i]=instructions[i]
pc=0
flag=False
while (pc < len(instructions)):
    jmpflag=False
    opcode=op[instructions[pc][:5]]
    if opcode in typeA:
        reg1=reg[instructions[pc][7:10]]
        reg2=reg[instructions[pc][10:13]]
        reg3=reg[instructions[pc][13:]]
        if opcode=="add":
            if add(regval,reg1,reg2,reg3):
                flag=True
        elif opcode=="sub":
            if sub(regval,reg1,reg2,reg3):
                flag=True
        elif opcode=="mul":
            if multiply(regval,reg1,reg2,reg3):
                flag=True
        elif opcode=="xor":
            xor(regval,reg1,reg2,reg3)
        elif opcode=="or":
            Or(regval,reg1,reg2,reg3)
        elif opcode=="and":
            And(regval,reg1,reg2,reg3)
        elif opcode=="addf":
            if addf(regval,reg1,reg2,reg3):
                flag=True
        elif opcode=="subf":
            if subf(regval,reg1,reg2,reg3):
                flag=True
        elif opcode=="nor":
            Nor(regval,reg1,reg2,reg3)
        elif opcode=="nand":
            Nand(regval,reg1,reg2,reg3)
        elif opcode=="xnor":
            Xnor(regval,reg1,reg2,reg3)
    elif opcode in typeB:
        reg1=reg[instructions[pc][6:9]]
        imm=int(instructions[pc][9:],2)
        if opcode=="movi":
            movImm(regval,reg1,imm)
        elif opcode=="rs":
            rshift(regval,reg1,imm)
        elif opcode=="ls":
            lshift(regval,reg1,imm)
        elif opcode=="movf":
            movf(regval,reg[instructions[pc][5:8]],instructions[pc][8:])
    elif opcode in typeC:
        reg1=reg[instructions[pc][10:13]]
        reg2=reg[instructions[pc][13:]]
        if opcode=="mov":
            movReg(regval,reg1,reg2)
        elif opcode=="div":
            if divide(regval,reg1,reg2):
                flag=True
        elif opcode=="not":
            invert(regval,reg1,reg2)
        elif opcode=="cmp":
            cmp(regval,reg1,reg2)
            flag=True
        elif opcode=="max":
            Max(regval,reg1,reg2)
        elif opcode=="min":
            Min(regval,reg1,reg2)
    elif opcode in typeD:
        reg1=reg[instructions[pc][6:9]]
        addr=int(instructions[pc][9:],2)
        if opcode=="ld":
            load(regval,memory,reg1,addr)
        elif opcode=="st":
            store(regval,memory,reg1,addr)
    elif opcode in typeE:
        addr=int(instructions[pc][9:],2)
        if opcode=="jmp":
            newpc=jmp(addr)
        elif opcode=="jlt":
            newpc=jlt(pc,regval,addr)
        elif opcode=="jgt":
            newpc=jgt(pc,regval,addr)
        elif opcode=="je":
            newpc=je(pc,regval,addr)
        if (newpc!=pc):
            jmpflag=True
    if not flag:
        regval["FLAGS"]="0000000000000000"
    else:
        flag=False
    print(format(pc,"07b"),end=" ")
    print("      ",end=" ")
    for value in regval.values():
        print(value,end=" ")
    print()
    if jmpflag:
        pc=newpc
    else:
        pc+=1
for instruction in memory:
    print(instruction)
