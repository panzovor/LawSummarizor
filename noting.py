
import matplotlib.pyplot as plt
import math
import random

def get_matric():
    leng = 13
    matrix =[[0]*leng for var in range(leng)]

    for i in range(leng):
        for j in range(i,leng):
            if i!=j:
                if i+6 == j:
                    continue
                if i in target1 and j in target1:
                    matrix[i][j] = random.randint(1,5)
                    matrix[j][i] = random.randint(1,5)
                elif i in target2 and j in target2:
                    matrix[i][j] = random.randint(1,3)
                    matrix[j][i] = random.randint(1,3)
                elif i in target3 and j in target3:
                    matrix[i][j] = random.randint(1,2)
                    matrix[j][i] = random.randint(1,2)
                else:
                    matrix[i][j] = random.randint(0,4)
                    matrix[j][i] = random.randint(0,4)

    for res in matrix:
        print(res)
    return matrix

def get_part_matrix(matirx,target_points):
    print(target_points)
    new_mat = [[0.0]*len(target_points) for var in range(len(target_points))]
    result = []
    for i in range(len(target_points)):
        for j in range(len(target_points)):
            if i!=j:
                for k in range(len(matirx)):
                    new_mat[i][j] += min(matirx[i][k],matirx[k][j])
                    result.append([i,k])
                    result.append([k,j])
    print(result)
    return new_mat


def show_matric(matric,name = None,special=False,color_r = None,color_b = None,color_g = None):
    thredshold = 0.0
    radio = 200
    x= []
    y= []
    angle = 360/len(matric)

    for i in range(len(matric)):
        x.append(radio*math.cos(math.radians(angle*(i+1))))
        y.append(radio*math.sin(math.radians(angle*(i+1))))
    used = []

    for i in range(len(matric)):
        for j in range(i,len(matric[i])):
            if matric[i][j]>thredshold and i!=j:
                linex = [x[i],x[j]]
                liney = [y[i],y[j]]
                if not special:
                    xx = (x[i]+x[j])/2
                    yy = (y[i]+y[j])/2
                else:
                    xx = (x[i]+x[j])/2-(20*i)
                    yy = (y[i]+y[j])/2-(20*i)
                if not special:
                    plt.annotate(str(matric[i][j]),xy=[xx,yy],xytext = [xx,yy])
                else:
                    plt.annotate(str(matric[i][j])+"("+str(name[i])+","+str(name[j])+")",xy=[xx,yy],xytext = [xx,yy])

                if color_r!=None and name == None and  i in color_r and j in color_r:
                    plt.plot(linex,liney,"r-")
                elif color_g!=None and name == None and i in color_g and j in color_g:
                    plt.plot(linex,liney,"g-")

                elif color_b!=None and name == None and  i in color_b and j in color_b:
                    plt.plot(linex,liney,"b-")
                else:
                    plt.plot(linex,liney,"k-")

                if color_r!=None and special:
                    plt.plot(linex,liney,"r-")
                elif color_g!=None and special:
                    plt.plot(linex,liney,"g-")

                elif color_b!=None and special:
                    plt.plot(linex,liney,"b-")

    if color_r!=None:
        plt.plot([-radio],[-radio],"r-",label ="Noun")
    if color_b!=None:
        plt.plot([-radio],[-radio],"b-",label ="Numeral")
    if color_g!=None:
        plt.plot([radio],[-radio],"g-",label ="Verb")
    if color_b!=None and color_g!=None and color_r!=None:
        plt.plot([radio],[radio],"k-",label ="DifferentRoles")
    plt.legend(loc="upper left")

    for i in range(len(x)):
        xx = (radio+20)*math.cos(math.radians(angle*(i+1)))
        yy = (radio+20)*math.sin(math.radians(angle*(i+1)))
        if name == None:
            plt.annotate(str(i),xy=[x[i],y[i]],xytext = [xx,yy])
        else:
            plt.annotate(str(name[i]),xy=[x[i],y[i]],xytext = [xx,yy])


    plt.scatter(x,y)

    plt.show()



target1 = [0,3,6,10,11]
target2 = [1,4,7,9]
target3 = [2,5,8,12]
# show_matric(get_matric(),color_r=target1,color_g=target2,color_b=target3)
# show_matric(get_part_matrix(get_matric(),target1),target1,special=True,color_r=target1)
# show_matric(get_part_matrix(get_matric(),target2),target2,special=True,color_g=target2)
# show_matric(get_part_matrix(get_matric(),target3),target3,special=True,color_b=target3)

with open("D:\workspace\LawSummarizor\\ddd") as file:
    content = file.readlines()[:13]
    matrix = []
    for lin in content:
        # print(lin)
        tmp = lin.strip()[1:-1].split(",")
        # print(tmp)
        matrix.append([int(var) for var in tmp])
    dd = 0
    for k in range(len(matrix)):
        if matrix[0][k]!=0 and matrix[k][3]!=0:
            print(0,"--",k,"--",3,matrix[0][k],matrix[k][3],min(matrix[0][k],matrix[k][3]))
            dd+= min(matrix[0][k],matrix[k][3])
    print(dd)