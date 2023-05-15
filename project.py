def movImm(regval,reg,temp):
    regval[reg]=format(int(temp),"016b")

def movReg(regval,reg1,reg2):
    regval[reg1]=regval[reg2]

def load(regval,reg,var,address):
    regval[reg]=var[address]

def store(regval,reg,var,address):
    var[address]=regval[reg]

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
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(prod,"016b")

def divide(regval,reg1,reg2):
    if regval[reg2]=="0000000000000000":
        regval["FLAGS"]="0000000000001000"
        regval["R0"]="0000000000000000"
        regval["R1"]="0000000000000000"
    else:
        regval["R0"]=format(int(regval[reg1][9:],2)//int(regval[reg2][9:],2),"016b")
        regval["R1"]=format(int(regval[reg1][9:],2)%int(regval[reg2][9:],2),"016b")
        regval["FLAGS"]="0000000000000000"

def add(regval, reg1, reg2, reg3):
    sum=int(regval[reg2][9:],2)+int(regval[reg3][9:],2)
    if sum>127:
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(sum,"016b")

def sub(regval, reg1, reg2, reg3):
    if int(regval[reg3],2)>int(regval[reg2],2):
        regval["FLAGS"]="0000000000001000"
        regval[reg1]="0000000000000000"
    else:
        regval["FLAGS"]="0000000000000000"
        regval[reg1]=format(int(regval[reg2],2)-int(regval[reg3],2),"016b")

def cmp(regval,reg1,reg2):
    if (regval[reg1]<regval[reg2]):
        regval["FLAGS"]="0000000000000100"
    elif (regval[reg1]>regval[reg2]):
        regval["FLAGS"]="0000000000000010"
    else:
        regval["FLAGS"]="0000000000000001"

def jlt(regval,pc,address,labels):
    if regval["FLAGS"][-3]=="1":
        pc=int(labels[address],2)
        return pc
    return pc+1

def jgt(regval,pc,address,labels):
    if regval["FLAGS"][-2]=="1":
        pc=int(labels[address],2)
        return pc
    return pc+1

def je(regval,pc,address,labels):
    if regval["FLAGS"][-1]=="1":
        pc=int(labels[address],2)
        return pc
    return pc+1

def jmp(pc,address,labels):
    pc=int(labels[address],2)
    return pc

op={"add":"00000","sub":"00001","movi":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
regval={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
var={}
mem={}
labels={}
error=False
f=open("test1.txt","r")
lines=[]
addresses={}
for line in f.readlines():
    if line.strip()!="":
        lines.append(line.strip())
f.close()
for i in range(len(lines)):
    if (i!=0) and (lines[i].strip().split()[0]=="var") and (lines[i-1].strip().split()[0]!="var"):
        error=True
        error_name=f"Error in line {i+1} : Variable not defined at beginning of code"
        break
i=0
for line in lines:
    index=bin(i)[2:]
    while (len(index)!=7):
        index="0"+index
    if line.split()[0]!="var":
        addresses[index]=line
        i+=1
for line in lines:
    index=bin(i)[2:]
    while (len(index)!=7):
        index="0"+index
    if line.split()[0]!="var":
        break
    addresses[index]=line
    i+=1
for i,j in addresses.items():
    if j.split()[0]=="var":
        mem[j.split()[1]]=i
    if ":" in j:
        cin=j.split()[0].index(":")
        labels[j.split()[0][:cin]]=i
temp=[]
f=open("test1.txt","r")
for line in f.readlines():
    if line.strip()!="" and line.strip().split()[0]!="var":
        temp.append(line.strip())
f.close()
ans=[]
hlt_count=0
line_no=len(mem)+1
for lines in temp:
    line=lines.split()
    t=""
    if ":" not in line[0]:
        if "add" in line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} in line {line_no} : add must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} in line no {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["add"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "sub" in line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} in line {line_no} : sub must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} in line no {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["sub"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif ("mov" in line[0]) and ("$"==line[2][0]):
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            elif "." in line[2][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (floating point number)"
                break
            elif int(line[2][1:])>127:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 7 bits)"
                break
            elif int(line[2][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["movi"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
        elif ("mov" in line[0]) and ("$"!=line[2][0]):
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["mov"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "ld" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : ld must contain 2 parameters"
                break
            elif (line[2] not in mem) and (line[2] not in labels):
                error=True
                error_name=f"Error in line {line_no} in line {line_no} : Use of undefined variable"
                break
            elif (line[2] not in mem) and (line[2] in labels):
                error=True
                error_name=f"Error in line {line_no} : Misuse of label as variable"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["ld"]+"0"+reg[line[1]]+mem[line[2]]
        elif "st" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : st must contain 2 parameters"
                break
            elif (line[2] not in mem) and (line[2] not in labels):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined variable"
                break
            elif (line[2] not in mem) and (line[2] in labels):
                error=True
                error_name=f"Error in line {line_no} : Misuse of label as variable"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["st"]+"0"+reg[line[1]]+mem[line[2]]
        elif "mul" in line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : mul must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["mul"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "div" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : div must contain 2 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["div"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "rs" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : rs must contain 2 parameters"
                break
            elif "." in line[2][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (floating point number)"
                break
            elif int(line[2][1:])>127:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 7 bits)"
                break
            elif int(line[2][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["rs"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
        elif "ls" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : ls must contain 2 parameters"
                break
            elif "." in line[2][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (floating point number)"
                break
            elif int(line[2][1:])>127:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 7 bits)"
                break
            elif int(line[2][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["ls"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
        elif "xor" in line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : xor must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["xor"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif ("xor" not in line[0]) and ("or" in line[0]):
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : or must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["or"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "and" in line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : and must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["and"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "not" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : not must contain 2 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["not"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "cmp" in line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : cmp must contain 2 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["cmp"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "jmp" in line[0]:
            if len(line)!=2:
                error=True
                error_name=f"Error in line {line_no} : jmp must contain 1 parameters"
                break
            elif (line[1] not in labels) and (line[1] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[1] not in labels) and (line[1] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jmp"]+"0000"+labels[line[1]]
        elif "jlt" in line[0]:
            if len(line)!=2:
                error=True
                error_name=f"Error in line {line_no} : jlt must contain 1 parameters"
                break
            elif (line[1] not in labels) and (line[1] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[1] not in labels) and (line[1] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jlt"]+"0000"+labels[line[1]]
        elif "jgt" in line[0]:
            if len(line)!=2:
                error=True
                error_name=f"Error in line {line_no} : jgt must contain 1 parameters"
                break
            elif (line[1] not in labels) and (line[1] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[1] not in labels) and (line[1] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jgt"]+"0000"+labels[line[1]]
        elif "je" in line[0]:
            if len(line)!=2:
                error=True
                error_name=f"Error in line {line_no} : je must contain 1 parameters"
                break
            elif (line[1] not in labels) and (line[1] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[1] not in labels) and (line[1] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["je"]+"0000"+labels[line[1]]
        elif "hlt" in line[0]:
            if len(line)!=1:
                error=True
                error_name=f"Error in line {line_no} : hlt must contain 1 parameters"
                break
            hlt_count+=1
            if line_no!=len(temp)+len(mem):
                error=True
                error_name=f"Error in line {line_no} : hlt not being used as the last intruction"
                break
            t+=op["hlt"]+"00000000000"
        else:
            error=True
            error_name=f"Error in line {line_no} : Typos in instruction name or register name"
            break
    else:
        if "add" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["add"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "sub" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["sub"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif ("mov" in line[1]) and ("$"==line[3][0]):
            if "." in line[3][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (floating point number)"
                break
            elif int(line[3][1:])>127:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 7 bits)"
                break
            elif int(line[3][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["movi"]+"0"+reg[line[2]]+format(int(line[3][1:]),"07b")
        elif ("mov" in line[1]) and ("$"!=line[3][0]):
            if line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["mov"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "ld" in line[1]:
            if (line[3] not in mem) and (line[3] not in labels):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined variable"
                break
            elif (line[3] not in mem) and (line[3] in labels):
                error=True
                error_name=f"Error in line {line_no} : Misuse of label as variable"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["ld"]+"0"+reg[line[2]]+mem[line[3]]
        elif "st" in line[1]:
            if (line[3] not in mem) and (line[3] not in labels):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined variable"
                break
            elif (line[3] not in mem) and (line[3] in labels):
                error=True
                error_name=f"Error in line {line_no} : Misuse of label as variable"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["st"]+"0"+reg[line[2]]+mem[line[3]]
        elif "mul" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["mul"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "div" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["div"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "rs" in line[1]:
            if "." in line[3][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (floating point number)"
                break
            elif int(line[3][1:])>127:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 7 bits)"
                break
            elif int(line[3][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["rs"]+"0"+reg[line[2]]+format(int(line[3][1:]),"07b")
        elif "ls" in line[1]:
            if "." in line[3][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (floating point number)"
                break
            elif int(line[3][1:])>127:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 7 bits)"
                break
            elif int(line[3][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["ls"]+"0"+reg[line[2]]+format(int(line[3][1:]),"07b")
        elif "xor" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["xor"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif ("xor" not in line[1]) and ("or" in line[1]):
            if (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["or"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "and" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["and"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "not" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["not"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "cmp" in line[1]:
            if (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            else:
                t+=op["cmp"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "jmp" in line[1]:
            if (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jmp"]+"0000"+labels[line[2]]
        elif "jlt" in line[1]:
            if (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jlt"]+"0000"+labels[line[2]]
        elif "jgt" in line[1]:
            if (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jgt"]+"0000"+labels[line[2]]
        elif "je" in line[1]:
            if (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["je"]+"0000"+labels[line[2]]
        elif "hlt" in line[1]:
            hlt_count+=1
            if line_no!=len(temp)+len(mem):
                error=True
                error_name=f"Error in line {line_no} : hlt not being used as the last intruction"
                break
            t+=op["hlt"]+"00000000000"
        else:
            error=True
            error_name=f"Error in line {line_no} : Typos in instruction name or register name"
            break
    ans.append(t)
    line_no+=1
if error:
    f=open("output.txt","w")
    f.write(error_name)
    f.close()
if not error:
    if hlt_count==0:
        error=True
        error_name="Error in line {line_no} : Missing hlt instruction in assembly code"
    if error:
        f=open("output.txt","w")
        f.write(error_name)
        f.close()
    else:
        pc=0
        flag=True
        while True:
            if flag:
                regval["FLAGS"]="0000000000000000"
            flag=True
            bin_pc=format(pc,"07b")
            if "hlt" in addresses[bin_pc]:
                break
            if ":" not in temp[pc].split()[0]:
                if ("mov" in temp[pc].split()[0]) and (temp[pc].split()[2][0]=="$"):
                    movImm(regval,temp[pc].split()[1],temp[pc].split()[2][1:])
                elif ("mov" in temp[pc].split()[0]) and (temp[pc].split()[2][0]!="$"):
                    movReg(regval,temp[pc].split()[1],temp[pc].split()[2])
                elif "add" in temp[pc].split()[0]:
                    add(regval,temp[pc].split()[1],temp[pc].split()[2],temp[pc].split()[3])
                    flag=False
                elif "sub" in temp[pc].split()[0]:
                    sub(regval,temp[pc].split()[1],temp[pc].split()[2],temp[pc].split()[3])
                    flag=False
                elif "ld" in temp[pc].split()[0]:
                    load(regval,temp[pc].split()[1],var,temp[pc].split()[2])
                elif "mul" in temp[pc].split()[0]:
                    multiply(regval,temp[pc].split()[1],temp[pc].split()[2],temp[pc].split()[3])
                    flag=False
                elif "div" in temp[pc].split()[0]:
                    divide(regval,temp[pc].split()[1],temp[pc].split()[2])
                    flag=False
                elif "st" in temp[pc].split()[0]:
                    store(regval,temp[pc].split()[1],var,temp[pc].split()[2])
                elif "cmp" in temp[pc].split()[0]:
                    cmp(regval,temp[pc].split()[1],temp[pc].split()[2])
                    flag=False
                elif "jlt" in temp[pc].split()[0]:
                    pc=jlt(regval,pc,temp[pc].split()[1],labels)
                    continue
                elif "jgt" in temp[pc].split()[0]:
                    pc=jgt(regval,pc,temp[pc].split()[1],labels)
                    continue
                elif "je" in temp[pc].split()[0]:
                    pc=je(regval,pc,temp[pc].split()[1],labels)
                    continue
                elif "jmp" in temp[pc].split()[0]:
                    pc=jmp(pc,temp[pc].split()[1],labels)
                    continue
            else:
                if ("mov" in temp[pc].split()[1]) and (temp[pc].split()[3][0]=="$"):
                    movImm(regval,temp[pc].split()[2],temp[pc].split()[3][1:])
                elif ("mov" in temp[pc].split()[1]) and (temp[pc].split()[3][0]!="$"):
                    movReg(regval,temp[pc].split()[2],temp[pc].split()[3])
                elif "add" in temp[pc].split()[1]:
                    add(regval,temp[pc].split()[2],temp[pc].split()[3],temp[pc].split()[4])
                    flag=False
                elif "sub" in temp[pc].split()[1]:
                    sub(regval,temp[pc].split()[2],temp[pc].split()[3],temp[pc].split()[4])
                    flag=False
                elif "ld" in temp[pc].split()[1]:
                    load(regval,temp[pc].split()[2],var,temp[pc].split()[3])
                elif "mul" in temp[pc].split()[1]:
                    multiply(regval,temp[pc].split()[2],temp[pc].split()[3],temp[pc].split()[4])
                    flag=False
                elif "div" in temp[pc].split()[1]:
                    divide(regval,temp[pc].split()[2],temp[pc].split()[3])
                    flag=False
                elif "st" in temp[pc].split()[1]:
                    store(regval,temp[pc].split()[2],var,temp[pc].split()[3])
                elif "cmp" in temp[pc].split()[1]:
                    cmp(regval,temp[pc].split()[2],temp[pc].split()[3])
                    flag=False
                elif "jlt" in temp[pc].split()[1]:
                    pc=jlt(regval,pc,temp[pc].split()[2],labels)
                    continue
                elif "jgt" in temp[pc].split()[1]:
                    pc=jgt(regval,pc,temp[pc].split()[2],labels)
                    continue
                elif "je" in temp[pc].split()[1]:
                    pc=je(regval,pc,temp[pc].split()[2],labels)
                    continue
                elif "jmp" in temp[pc].split()[1]:
                    pc=jmp(pc,temp[pc].split()[2],labels)
                    continue
            pc+=1
        f=open("output.txt","w")
        for i in ans:
            f.write(i+"\n")
        f.close()

