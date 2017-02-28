__author__ = 'E440'
import Tools
import src1.DataLoader as dataloader
import Dir
import re

label = ["<经审理查明>","</经审理查明>"]

def load_parameter(filepath = Dir.resourceDir+"paragraph_parameter.csv"):
    parameter ={}
    with open(filepath,mode="r",encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            tmp = line.split(",")
            if tmp.__len__() !=3:
                string_regex = str(tmp[1:-1])[1:-1].replace("', '",",")
                string_regex = string_regex.replace("'","")
                new_tmp = [tmp[0],string_regex,tmp[-1]]
            else:
                new_tmp = tmp
            if new_tmp[0] not in parameter.keys():
                parameter[new_tmp[0]] = {}
            parameter[new_tmp[0]][new_tmp[1]] = float(new_tmp[2].strip())
    return parameter

para_parameter = load_parameter()

def combine_rule(rules):
    regex =""
    for rule,order in rules.items():
        regex+="("+rule+")|"
    regex =regex[:-1]
    return regex

def locate_paragraphs(contents):
    before_lines =[]
    after_lines=[]
    for content in contents:
        tmp = locate_paragraph(content)
        before_lines.append(tmp[0])
        after_lines.append(tmp[1])
    # for lines in before_lines:
    #     print(lines)
    # for lines in after_lines:
    #     print(lines)
    return before_lines,after_lines

def locate_paragraph(content):
    content = str(content)
    if label[0] in content and label[1] in content :
        index_start = content.index(label[0])
        index_end = content.index(label[1])
        before_content = content[:index_start+label[0].__len__()+20]
        after_content = content[index_end:]
        before_lines = Tools.seperate_sentences(before_content)
        after_lines = Tools.seperate_sentences(after_content)
        # print("before",before_lines[-1].replace("\n",""),end="\t")
        # print("after",str(after_lines[0:2]).replace("\n",""))
    else:
        # print("null")
        before_lines= ["null"]
        after_lines= ["null"]
    return before_lines[-1],after_lines[0]

# 典型案例111篇
# 基础案例299篇-已标注
def first_filter():
    file_dir = Dir.resourceDir+"/已标注文书-txt/paragraph_labeled/"
    # save_dir = Dir.resourceDir+"/已标注文书-txt/paragraph_labeled/"
    # print(file_dir)
    data = dataloader.get_all_data(file_dir)[2]
    datas = []
    # print(data.items().__len__())
    count=0
    for name,content in data.items():
        datas.append(content)
        # print(name,end="\t")
        result = locate_paragraph(content)
        # print(result[0])
        if result[0] == "null":
            continue
        count+=1
        # with open(save_dir+name+".txt",mode="w",encoding="utf-8") as file:
        #     file.write(content)
    # print("labeled file num", count)
# first_filter()

def extract_sentence(content):
    regex = label[0]+"[\s\S]*?"+label[1]
    label_regex= [[label[0],regex]]
    result = dataloader.labeled_text(content,label_regex)
    new_result ={}
    for sen in result.keys():
        new_sen =re.sub("<.*?>","",sen)
        new_sen = new_sen.strip()
        if new_sen.__len__() == 0:
            continue
        new_result[new_sen] = result[sen]
    return new_result

def preprocess(content):
    content = dataloader.pre_process(content)
    content = content.replace("\n","##")
    content = re.sub("#+","#",content)
    return content

debug = False

def simple(content):
    content = preprocess(content)
    content = re.sub("<.*?>","",content)
    result =[]
    sentences = Tools.seperate_sentences(content)
    start_rules = para_parameter["start"]
    end_rules = para_parameter["end"]
    start_index,end_index = [],[]
    start_rule_all = combine_rule(para_parameter["start"])
    end_rule_all = combine_rule(para_parameter["end"])
    for i in range(sentences.__len__()):
        sen= sentences[i]
        for start_rule,s_order in start_rules.items():
            # print(start_rule,start_rule_all)
            if re.findall(start_rule,sen).__len__()>0 and re.findall(end_rule_all,sen).__len__()<=0:
                start_index.append([i,s_order])
        for end_rule,e_order in end_rules.items():
            # print(end_rule,sen)
            if re.findall(end_rule,sen).__len__()>0 and re.findall(start_rule_all,sen).__len__()<=0:

                end_index.append([i,e_order])
    if debug:
        print("st_len",start_index)
    if start_index.__len__()==0:
        start_index=0
    else:
        tmp = sorted(start_index,key = lambda d:d[1])[0]
        # first_order = tmp[1]
        # print(first_order)
        tmp_index =[]
        for sen_index,order in start_index:
            if order == tmp[1]:
                tmp_index.append(sen_index)
        if debug:
            print(tmp_index)
        start_index =sorted(tmp_index,reverse=False)[0]

        # print(start_index)


    if debug:
        print("en_len",end_index)
    if end_index.__len__() ==0:
        end_index =sentences.__len__()
    else:
        # for sen_index,order in end_index:
        #     if sen_index> start_index:
        #         end_index = sen_index
        # if isinstance(end_index,list):
        #     end_index = sentences.__len__()
        tmp = sorted(end_index,key = lambda d:d[1])[0]
        # first_order = tmp[1]
        tmp_index =[]
        for sen_index,order in end_index:
            if order == tmp[1]:
                tmp_index.append(sen_index)
        if debug:
            print(tmp_index)
        end_index =sorted(tmp_index,reverse=True)[0]
        if end_index<start_index:
            end_index = sentences.__len__()
    if debug:
        print(start_index,end_index)
    # print(start_index,end_index)
    result.extend(sentences[start_index:end_index])
    # print(start_index,end_index)
    if debug:
        for res in result:
            print(res)

    return result

def compare(standard,answer):
    # count =0
    # standard_only,answer_only,both = [],[],[]
    standard_only = set(standard)-set(answer)
    answer_only = set(answer)-set(standard)
    both = set(standard).intersection(set(answer))
    return sorted(standard_only),sorted(answer_only),sorted(both)

def calculate(standard,answer):
    s_only,a_only,both = compare(standard,answer)
    # print(s_only.__len__(),a_only.__len__(),both.__len__())
    # return both.__len__()/answer.__len__(),both.__len__()/standard.__len__()
    return both.__len__(),answer.__len__(),standard.__len__()
def locate(content):
    result = extract_sentence(content)
    standard = []
    for sen in result.keys():
        if isinstance(result[sen],str):
            standard.append(sen)
    answer = simple(content)

    sorted_standard = sorted(standard)
    sorted_answer = sorted(answer)
    try:
        both,precison,recall = calculate(sorted_standard,sorted_answer)
    except:
        print(sorted_standard)
        print("-========================-")
        print(sorted_answer)
        input()
    return  both,precison,recall

def demo():
    dir_classic = Dir.resourceDir+"已标注文书-txt/paragraph_labeled/"
    classic,all_labeled,origindata = dataloader.get_all_data(dir_classic)
    result =[]
    for name,content in origindata.items():
        # print(name)
        both,precision,recall = locate(content)
        result.append([both,precision,recall])
    for res in result:
        print(res)
    both = sum([n for n,var,var1 in result])
    preci = sum([var for n,var,var1 in result])
    recall = sum(var for n,vav1,var in result)

    precision = both/preci
    recall_ = both/recall
    f_score = 2*precision*recall_/(precision+recall_)
    print(precision,recall_,f_score)

def single(name):
    dir_classic = Dir.resourceDir+"已标注文书-txt/paragraph_labeled/"
    classic,all_labeled,origindata = dataloader.get_all_data(dir_classic)
    # name = "2-广东美的生活电器制造有限公司与梅霞侵害商标权纠纷一审民事判决书"
    content = origindata[name]
    simple(content)

demo()
# name ="(2010)民提字第27号"
# debug=True
# single(name)

