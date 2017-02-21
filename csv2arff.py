

def convert(filepath,savepath):
    content = "@relation train_file\n"
    with open(filepath,mode="r") as file:
        lines = file.readlines()

        for i in range(lines.__len__()):
            if i  == 0:
                tmp = lines[0].split(",")
                for j in range(tmp.__len__()-1):
                    tmp_string = tmp[j]
                    content+= "@attribute "+tmp_string+" numeric\n"
                content+="@attribute class {0,1}\n@data \n"
            else:
                content+=str(lines[i])[:-1]+"\n"
    with open(savepath,mode="w") as file:
        file.write(content)

convert("/home/czb/workspace/Summarizor/src1/train.csv","/home/czb/workspace/Summarizor/src1/train.arff")
