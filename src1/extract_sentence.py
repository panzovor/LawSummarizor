import src1.DataLoader as dataLoader
import Dir
import re

def filter(content):
    names = ['原告经营情况','企业名称变更','注册商标权利情况','证明商标使用管理规则','商标许可/转让情况','商标共有情况','商标知名度','驰名商标','申请驰名商标司法认定','证据保全公证','著作权登记','著作权归属','被告经营情况','行为人商标使用情况','与域名相关的事实','贴牌加工行为','合法来源','未实际使用','商标行政程序','商标权行政诉讼','商标权行政处罚','商标权犯罪']
    names.extend(['合理开支','产品利润','违法收入','原产地域名称情况'])
    regex = ""
    for name in names:
        regex+="</{0,1}"+name+">|"
    regex = regex[:-1]
    content = re.sub(regex,"",content)
    return content



def transfer(dir,two_class = True,label_file = Dir.resourceDir+"标签-paragraph.csv"):
    data  = dataLoader.get_all_data(dir)[2]
    result = []
    seperate = "\t"
    label_regex = dataLoader.get_label_regex(dataLoader.read_label(label_file))
    for name,content in data.items():
        labeled_content = dataLoader.labeled_text(content,label_regex=label_regex,filter=filter)
        if two_class :
            tmp =[]
            for sen in labeled_content.keys():
                sentence = sen.strip()
                if sentence == "":
                    continue
                if labeled_content[sen].__len__()>0:
                    result.append(sentence + seperate + "1" + '\n')

                    tmp.append(sentence + seperate + "1" + '\n')
                else:
                    result.append(sentence + seperate + "0" + '\n')
                    tmp.append(sentence + seperate + "0" + '\n')
            # check_res = check_transfer_details(tmp)
            # if check_res.__len__()>0:
            #     print(name)
            #     print(check_res)
        else:
            for sen in labeled_content.keys():
                sentence = sen.strip()
                if sentence == "":
                    continue
                if labeled_content[sen].__len__()>0:
                    result.append(sentence + seperate+labeled_content[sen]+'\n')
                else:
                    result.append(sentence+seperate+"null"+"\n")
    return result

def save(content_list,savepath):
    with open(savepath,mode="w") as file:
        file.writelines(content_list)

def check(filepath):
    with open(filepath,mode="r") as file:
        content = file.readlines()
    # print(content.__len__())
    count=0
    for line in content:
        tmp = line.split("\t")
        if tmp.__len__()>2:
            print(tmp)
            print(count)
            count+=1

def check_if_contain(filepath):
    data  = dataLoader.get_all_data(filepath)[2]
    counter =[0,0,0,0]
    result = [[],[],[],[]]
    for name, content in data.items():
        if "..." in content:
            counter[0]+=1
            result[0].append(content)
        if "......" in content:
            counter[-1]+=1
            result[-1].append(content)
        if "。。。" in content:
            counter[1]+=1
        if "。。。。。。" in content:
            content[2]+=1
    print("...","......","。。。","。。。。。。")
    print(counter)

    for cont in result[-1]:
        print(cont)

def check_transfer(content):
    counter = [0,0]
    for line in content:
        tmp = line.split("\t")
        string = ''.join(tmp[:-1])
        if string.__len__() <=4:
            print(string,tmp[-1].strip())
        # print(tmp[-1])
        if "1" in tmp[-1]:
            counter[1]+=1
        elif "0" in tmp[-1]:
            counter[0]+=1
    print(counter,sum(counter))
    print(content.__len__())


def check_transfer_details(content):
    counter = [0,0]
    tmp_result= []
    for line in content:
        tmp = line.split("\t")
        string = ''.join(tmp[:-1])
        if string.__len__() <=4:
            tmp_result.append(string+","+str(tmp[-1].strip()))
        # print(tmp[-1])
        if "1" in tmp[-1]:
            counter[1]+=1
        elif "0" in tmp[-1]:
            counter[0]+=1
    return tmp_result
    # print(counter,sum(counter))
    # print(content.__len__())

def extract_label_data(dir,save_dir):
    data  = dataLoader.get_all_data(dir)[2]
    result = {}
    for name,content in data.items():
        labeled_content = dataLoader.labeled_text(content)
        for sentence,label in labeled_content.items():
            if isinstance(label,str):
                if label not in result.keys():
                    result[label] =[]
                result[label].append(sentence+"\n")
            else:
                if "null" not in result.keys():
                    result["null"] =[]
                result["null"].append(sentence+"\n")
    for label in result.keys():
        name = label
        if "/" in label:
            name = label.replace("/","")
        savepath = save_dir+"/"+name+".txt"
        with open(savepath,mode="w",encoding="utf-8") as file:
            file.writelines(result[label])


import Dir
# 典型案例111篇
# 基础案例299篇-已标注
dir_classic = Dir.resourceDir+"已标注文书-txt/paragraph_labeled/"
content = transfer(dir_classic,two_class=False)
savepath =  Dir.projectDir+"/src1_result/new_extract_data/data_labeled_two"
print(content.__len__())
save(content,savepath)

# save_dir =  Dir.projectDir+"/src1_result/label_data/all"
# extract_label_data(dir_classic,save_dir)

# check(savepath)
# check_transfer(content)