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

op={"add":"00000","sub":"00001","movi":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010","addf":"10000","subf":"10001","movf":"10010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
regval={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
var={}
mem={}
labels={}
error=False
lines=[]
test=sys.stdin.readlines()
addresses={}
for line in test:
    if line.strip()!="":
        lines.append(line.strip())
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
        var[j.split()[1]]="0000000"
    if ":" in j:
        cin=j.split()[0].index(":")
        labels[j.split()[0][:cin]]=i
temp=[]
for line in test:
    if line.strip()!="" and line.strip().split()[0]!="var":
        temp.append(line.strip())
ans=[]
hlt_count=0
line_no=len(mem)+1
for lines in temp:
    line=lines.split()
    t=""
    if ":" not in line[0]:
        if "add" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : add must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["add"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "sub" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : sub must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} in line no {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["sub"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif ("mov" == line[0]) and ("$"==line[2][0]):
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
            elif line[1] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["movi"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
        elif ("mov" == line[0]) and ("$"!=line[2][0]):
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["mov"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "ld" == line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : ld must contain 2 parameters"
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
            elif line[1] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["ld"]+"0"+reg[line[1]]+mem[line[2]]
        elif "st" == line[0]:
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
            elif line[1] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["st"]+"0"+reg[line[1]]+mem[line[2]]
        elif "mul" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : mul must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["mul"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "div" == line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : div must contain 2 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["div"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "rs" == line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : rs must contain 2 parameters"
                break
            elif line[2][0]!="$":
                error=True
                error_name=f"Error in line {line_no} : Immediate value not definrd correctly"
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
            elif line[1] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["rs"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
        elif "ls" == line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : ls must contain 2 parameters"
                break
            elif line[2][0]!="$":
                error=True
                error_name=f"Error in line {line_no} : Immediate value not definrd correctly"
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
            elif line[1] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["ls"]+"0"+reg[line[1]]+format(int(line[2][1:]),"07b")
        elif "xor" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : xor must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["xor"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "or" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : or must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["or"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "and" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : and must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["and"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "not" == line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : not must contain 2 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["not"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "cmp" == line[0]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : cmp must contain 2 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["cmp"]+"00000"+reg[line[1]]+reg[line[2]]
        elif "jmp" == line[0]:
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
        elif "jlt" == line[0]:
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
        elif "jgt" == line[0]:
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
        elif "je" == line[0]:
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
        elif "addf"==line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : add must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["addf"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif "subf" == line[0]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : sub must contain 3 parameters"
                break
            elif (line[1]=="FLAGS") or (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} in line no {line_no} : Illegal use of FLAGS register"
                break
            elif (line[1] not in reg) or (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["subf"]+"00"+reg[line[1]]+reg[line[2]]+reg[line[3]]
        elif ("movf" == line[0]):
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            elif "." not in line[2][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value not a floating point number"
                break
            num=floattobin(float(line[2][1:]))
            if len(num)>8:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 8 bits)"
                break
            elif float(line[2][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[1]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif line[1] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["movi"]+reg[line[1]]+(8*'0')+num
        elif "hlt" == line[0]:
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
        
        if "add" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : add must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["add"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "sub" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : sub must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["sub"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif ("mov" == line[1]) and ("$"==line[3][0]):
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            elif "." in line[3][1:]:
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
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["movi"]+"0"+reg[line[2]]+format(int(line[3][1:]),"07b")
        elif ("mov" == line[1]) and ("$"!=line[3][0]):
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            if line[3] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["mov"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "ld" == line[1]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : ld must contain 2 parameters"
                break
            elif (line[3] not in mem) and (line[3] not in labels):               
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
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["ld"]+"0"+reg[line[2]]+mem[line[3]]
        elif "st" == line[1]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : st must contain 2 parameters"
                break
            elif (line[3] not in mem) and (line[3] not in labels):
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
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["st"]+"0"+reg[line[2]]+mem[line[3]]
        elif "mul" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : mul must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["mul"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "div" == line[1]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : div must contain 2 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["div"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "rs" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : rs must contain 2 parameters"
                break
            elif line[3][0]!="$":
                error=True
                error_name=f"Error in line {line_no} : Immediate value not definrd correctly"
                break
            elif "." in line[3][1:]:
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
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["rs"]+"0"+reg[line[2]]+format(int(line[3][1:]),"07b")
        elif "ls" == line[1]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : ls must contain 2 parameters"
                break
            elif line[3][0]!="$":
                error=True
                error_name=f"Error in line {line_no} : Immediate value not definrd correctly"
                break
            elif "." in line[3][1:]:
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
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["ls"]+"0"+reg[line[2]]+format(int(line[3][1:]),"07b")
        elif "xor" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : xor must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["xor"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "or" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : or must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["or"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "and" == line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : and must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["and"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "not" == line[1]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : not must contain 2 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["not"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "cmp" == line[1]:
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : cmp must contain 2 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["cmp"]+"00000"+reg[line[2]]+reg[line[3]]
        elif "jmp" == line[1]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : jmp must contain 1 parameters"
                break
            elif (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jmp"]+"0000"+labels[line[2]]
        elif "jlt" == line[1]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : jlt must contain 1 parameters"
                break 
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
        elif "jgt" == line[1]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : jgt must contain 1 parameters"
                break
            elif (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["jgt"]+"0000"+labels[line[2]]
        elif "je" == line[1]:
            if len(line)!=3:
                error=True
                error_name=f"Error in line {line_no} : hlt must contain 1 parameters"
                break
            elif (line[2] not in labels) and (line[2] not in mem):
                error=True
                error_name=f"Error in line {line_no} : Use of undefined label"
                break
            elif (line[2] not in labels) and (line[2] in mem):
                error=True
                error_name=f"Error in line {line_no} : Misuse of variable as label"
                break
            else:
                t+=op["je"]+"0000"+labels[line[2]]
        elif "addf"==line[1]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : add must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["addf"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif "subf" == line[0]:
            if len(line)!=5:
                error=True
                error_name=f"Error in line {line_no} : sub must contain 3 parameters"
                break
            elif (line[2]=="FLAGS") or (line[3]=="FLAGS") or (line[4]=="FLAGS"):
                error=True
                error_name=f"Error in line {line_no} in line no {line_no} : Illegal use of FLAGS register"
                break
            elif (line[2] not in reg) or (line[3] not in reg) or (line[4] not in reg):
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["subf"]+"00"+reg[line[2]]+reg[line[3]]+reg[line[4]]
        elif ("movf" == line[1]):
            if len(line)!=4:
                error=True
                error_name=f"Error in line {line_no} : mov must contain 2 parameters"
                break
            elif "." not in line[3][1:]:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value not a floating point number"
                break
            num=floattobin(float(line[3][1:]))
            if len(num)>8:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (more than 8 bits)"
                break
            elif float(line[3][1:])<0:
                error=True
                error_name=f"Error in line {line_no} : Illegal immediate value (-ve number)"
                break
            elif line[2]=="FLAGS":
                error=True
                error_name=f"Error in line {line_no} : Illegal use of FLAGS register"
                break
            elif line[2] not in reg:
                error=True
                error_name=f"Error in line {line_no} : Invalid register name"
                break
            else:
                t+=op["movi"]+reg[line[2]]+(8*'0')+num
        elif "hlt" == line[1]:
            if len(line)!=2:
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
            error_name=f"Error in line {line_no} : Typos in instruction name"
            break
    ans.append(t)
    line_no+=1
if error:
    print(error_name)
if not error:
    if hlt_count==0:
        error=True
        error_name="Error : Missing hlt instruction in assembly code"
    if error:
        print(error_name)
    else:
        for i in ans:
            print(i)


