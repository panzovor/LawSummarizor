__author__ = 'E440'
import Dir
import Tools
import re


### input: file path of label file
### output: [[label name, label start, label end],...,[labeln, labeln start, labeln end]]
def read_label(filename):
    label_data = []
    with open(filename,mode="r",encoding="utf-8") as file:
        for line in file.readlines():
            line = line.strip()
            tmp = line.split(",")
            label_data.append(tmp)
    return label_data

def get_label_regex(label_info):
    label_regex ={}
    # for label in label_info:
    #     label_regex[label[0]] = label[0].__len__()
    # label_regex =  sorted(label_regex.items(),key = lambda  d:d[1],reverse = True)
    # result =[]
    # for label,val in label_regex:
    #     result.append([label,"<.*?"+label+".*?>" +"(.*?)"+"</.*?"+label+".*?>"])

    for label in label_info:
        label_regex[label[0]]= "<.*?"+label[0]+".*?>" +"(.*?)"+"</.*?"+label[0]+".*?>"
    result =  sorted(label_regex.items(),key = lambda  d:d[1],reverse = True)
    return result

file = Dir.resourceDir+"标签-sheet1.csv"
label_info = read_label(file)
label_regex = get_label_regex(label_info)

def remove_label_sentences(content,label_regex = label_regex):
    result = content
    for label,regex in label_regex:
        # print(regex)
        result = re.sub(regex,"",result)
    return result

def pre_process(string):
    regex = "：(?:.*?；)+"
    seperate = re.findall(regex,string)
    value = re.split(regex,string)
    string_result = ""
    if value.__len__()>1 and  seperate.__len__()==  value.__len__()-1:
        for i in range(value.__len__()):
            string_result+= value[i]
            if i < value.__len__()-1:
                string_result+= seperate[i].replace("；","@")
    else:
        string_result=string
    return string_result

def nothing(content):
    return content
### input : a text
### output: a dict with sentence and its label({})
def labeled_text(content,label_regex = label_regex,filter = nothing):
    content = pre_process(content)
    content = content.replace("\n","##")
    content = re.sub("#+","#",content)
    content = filter(content)
    process_result= process_tag_file(content,label_regex = label_regex)
    result ={}
    for label,sentences in process_result.items():
        for sentence in sentences:
            result[sentence] = label
    num = result.__len__()
    content = remove_label_sentences(content,label_regex = label_regex)
    all_sentences = Tools.seperate_sentences(content)
    for sen in all_sentences:
        if sen not in result.keys():
            result[sen] = []
    return result

### input : a text
### output: a dict with sentence and its label({})
# def labeled_text_new(content):
#     process_result= process_tag_file(content)
#     result ={}
#     for label,sentences in process_result.items():
#         for sentence in sentences:
#             result[sentence] = label
#     num = result.__len__()
#     content = remove_label_sentences(content)
#     all_sentences = seperate_sentences(content)
#     for sen in all_sentences:
#         if sen not in result.keys():
#             result[sen] = []
#     return result

def seperate_sentences(content):
    regex = "。|？|！|；"
    tmp = re.split(regex,content)
    result = []
    for tmp_string in tmp:
        if tmp_string.strip().__len__()<2:
            continue
        result.append(tmp_string.strip())
    return result
### input : a text
### output: a dict with sentence and its label(dict)
# def labeled_text_correct(content):



### input: tag file
### output: a dict with label as key and its sentences as value({"label":[sentence1,..,sentencem],.., "labelk":[sentencek1,..,sentencekm]})

def process_tag_file(content,label_regex= label_regex):
    process_result = {}
    for label,regex in label_regex:
        label_sentences = re.findall(regex,content)
        if label not in process_result.keys() and label_sentences.__len__()>0:
            label_sentences_seperate = []
            for label_sentence in label_sentences:
                label_sentences_seperate.extend(Tools.seperate_sentences(label_sentence))
            process_result[label]=label_sentences_seperate
    return process_result

def remove_all_label(content ,label_info=label_info):
    result = content
    for label in label_info:
        result = result.replace(label[1],"")
        result = result.replace(label[2],"")
    return result


### get the input data and its corresponding answers
### input: the dir of input data(labeled data)
### output: a tuple
### output1: a dict with filename as its keys and all labels and its correponding sentences
###          e.g. {filename1: {label1: value1,...,labeln:valuen},..,filenamen: {label1: value1,...,labeln:valuen}}
### output2: a dict with labels as keys and its corresponding sentences as value
###          e.g. {"label":[sen1,..,senn],...,"labeln":[sen1,..,senn]}
### output3: a dict with filename as its keys and content as value
def get_all_data(dir_labeled):
    filelist_labeled = []
    Tools.get_filelist(dir_labeled,filelist_labeled)
    data = {}
    all_labeled_data ={}
    origin_data ={}
    for filename in filelist_labeled:
        with open(filename,encoding="utf-8") as file:
            content = file.read()
            tag_sentences = process_tag_file(content)
            origin = remove_all_label(content)
            for key in tag_sentences:
                if key not in all_labeled_data.keys():
                    all_labeled_data[key] = []
                if ' ' in tag_sentences[key]:
                    tag_sentences[key].remove(' ')
                if '' in tag_sentences[key]:
                    tag_sentences[key].remove('')

                all_labeled_data[key].extend(tag_sentences[key])
            name = Tools.get_filename(filename)[:-4]
            data[name] = [origin,tag_sentences]
            origin_data[name] = content
    return data,all_labeled_data,origin_data

def demo():
    dir_classic = Dir.resourceDir+"已标注文书-txt/典型案例111篇3/"
    classic,all_labeled,origindata = get_all_data(dir_classic)
    dir_basic = Dir.resourceDir+"已标注文书-txt/基础案例299篇-已标注/"
    basic = get_all_data(dir_basic)
