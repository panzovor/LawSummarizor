import math

def judge(num):
    log_i = int(math.log(float(num),2.0))+1
    for i in range(1,log_i+1):
        bas = int(math.pow(float(num),1/i))
        if int(math.pow(bas,i)) == num and judgez(bas):
            return str(bas)+" "+str(i)
    return "No"

def judgez(num):
    for i in range(2,int(math.pow(num,2.0))+1):
        if num%i == 0 and i<num:
            return False
    return True

# try:
while 1:
    n = int(input())
    print(judge(n))
# except:
#     pass