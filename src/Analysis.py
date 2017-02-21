__author__ = 'E440'
import jieba
import jieba.posseg as pog
import src.DataLoader as dataloader
import Dir
import Tools
import re
import math
import numpy as np
### input: data of single label (list)
### output: analysis reesult of data
### analysis result:
###    1. num
###    2. sentences average length
###    3. entrys(people name ,place, company, time) of data
###    4. num of noun
###    5. num of verb
###    6. tf of very words
def analsis_single_label_data(data):
    num = data.__len__()
    average = 0
    noun_num,verb_num = 0,0
    words_tf = {}
    for sentence in data:
        average+= sentence.__len__()
        words = pog.cut(sentence)
        for word, pos in words.items():
            if "n" in pos:
                noun_num+=1
            if "v" in pos:
                verb_num+=1
            if word not in words_tf.keys():
                words_tf[word] = 0
            words_tf[word]+=1

    average/= num
    noun_num/=num
    verb_num/=num
    words_tf=sorted(words_tf.items(), key = lambda d: d[1],reverse = True)
    return num,average,noun_num,verb_num,words_tf

def save_result(content,filepath):
    with open(filepath,mode = "w") as file:
        file.write(content)
        file.close()

### transfer a text to an arff file format
### input: text(string)
### output: a arff string
def transfer2_arff(data):
    labeled_data = dataloader.labeled_text(data)
    arff_string ="@ summarization\n@ attribute num\n@ attribute avelen\n" \
                 "@ attribute entrys\n@attribute num_noun\n@ num of verb\n" \
                 "@attribute tfidf\n@data\n"
    for sentence in labeled_data.keys():
        features = analysis_single_sentences(sentence)
        sentence_feature =""
        for feature in features:
            if isinstance(features,list):
                for value in feature:
                    sentence_feature+=str(value)+" "
            else:
                sentence_feature+= str(feature)+" "
        for label in labeled_data[sentence]:
            arff_string+= sentence+label+"\n"
    return arff_string

### transfer a text to an arff file format( only 2 clas: 0,1(means that sentence is label,but don't care what label is))
### input: text(string)
### output: a arff string
''' arff_title = "@ summarization\n@ attribute num\n@ attribute avelen\n" \
                 "@ attribute entrys\n@attribute num_noun\n@ num of verb\n" \
                 "@attribute tfidf\n@data\n"
'''
def transfer2arff_simple(data,tfidfs):
    labeled_data = dataloader.labeled_text(data)
    arff_string =""
    for sentence in labeled_data.keys():
        if sentence.strip().__len__() == 0:
            continue
        features = analysis_single_sentences_simple(sentence,tfidfs)
        sentence_feature =""
        for feature in features:
            if isinstance(features,list):
                for value in feature:
                    sentence_feature+=str(value)+","
            else:
                sentence_feature+= str(feature)+","
        print(sentence_feature)
        if labeled_data[sentence].__len__()>0:
            arff_string+= sentence_feature+"1\n"
        else:
            arff_string+= sentence_feature+"0\n"
        arff_string = arff_string.replace(" (",", ")
        arff_string = arff_string.replace(") [[",", ")
        arff_string = arff_string.replace("], [",", ")
        arff_string = arff_string.replace("]] ",", ")
        arff_string = arff_string.replace("]]",", ")
        arff_string = arff_string.replace("[[",", ")
        arff_string = arff_string.replace("(",", ")
        arff_string = arff_string.replace(")",", ")

    return arff_string

### input: a dict with format of output2 of DataLodaer.get_all_data
###        e.g. {"label":[sen1,..,senn],...,"labeln":[sen1,..,senn]}， label can be 2 class or detail class
### output: tf_idf of all labels's words
###        e.g. {"label1":{"word1":tfidf1,...,"wordn":tfidfn},...,"labeln":{"word1":tfidf1,...,"wordn":tfidfn}}
### details:  1. preprocess all the sentences (replace time words, law_words)
###           2. combine all sentences shared same label as a text
###           3. compute all the words's tf_idf
### parameter: save_dir(a dictionary to save tf_idf file with csv format named by label)
###           e.g. "c:/data/"
def build_tfidf(data,save_dir = Dir.resourceDir+"tfidf/"):
    ### output: {label:{word1: tf_idf1},...,{wordn:tf_idfn},...,{labeln:{word1:tf_idf,..,{wordn:tf_idfn}}}}
    result = {}
    for label, sentences in data.items():
        if label not in result :
            result[label] = {}
        for sentence in sentences:
            sentence = preprocess_data(sentence)
            words  = list(jieba.cut(sentence))

            for word in words:
                if " " == word:
                    continue
                if word not in result[label].keys():
                    result[label][word] = 0.
                result[label][word]+=1.

    new_result = result.copy()
    for label,words in result.items():
        all= sum(words.values())

        for word,tf in words.items():
            idf =0.0
            for label1 in result.keys():
                if word in result[label1].keys():
                    idf+=1
            new_result[label][word] /= all
            new_result[label][word] *= math.log(result.__len__()/idf)

    if save_dir != None:
        for label,words in new_result.items():
            content = ""
            if "/" in label:
                label = label.replace("/",'')
            save_path = save_dir+label
            words = sorted(words.items(),key = lambda  d:d[1],reverse = True)

            for word,tfidf in words:
                content+= word+" "+str(tfidf)+"\n"
            save_result(content,save_path)

    return new_result,result
dataloader
time_regex = "(.{1,4}年.{1,2}月.{1,2}日)|(.{1,2}月.{1,2}日)"
law_regex = "(《.*?》)"
x_regex = "\*+"

### input: a sentence
### output: a sentence that all time words and law_words is replaced with " 时间  "," 法律 "
def preprocess_data(sentence):

    # | \"\*?\"
    sentence_ =re.sub(time_regex," 时间 ",sentence)
    sentence_ =re.sub(law_regex," 法律 ",sentence_)
    sentence_ =re.sub(x_regex,"实体",sentence_)
    return sentence_

### get feature from a sentence
### input: sentence(string)
###        tfidfs: output of build_tfidf
###        e.g. {"label1":{"word1":tfidf1,...,"wordn":tfidfn},...,"labeln":{"word1":tfidf1,...,"wordn":tfidfn}}
### output: features of input sentence(list)
### features:
###    1. num of words
###    2. sentences average length
###    3. entrys(people name ,place, company, time) of data
###    4. num of noun
###    5. num of verb
###    6. tf of very words
def analysis_single_sentences_simple(sentence,tfidfs):
    # print(sentence)
    if sentence.strip().__len__() == 0:
        return None
    t = pog.cut(sentence)
    # print(t)
    words_only = []
    for w,tag in t:
        # print(w)
        words_only.append(w)
    # words = list(t)
    # print(t.__len)
    num = words_only.__len__()
    num_noun =0
    num_verb = 0
    for word,tag in t:
        if "n" in tag:
            num_noun+=1
        if "v" in tag:
            num_verb+=1
    law_regex = "(《.*?》)"
    company_regex ="公司|法人"
    # time_regex = "(.*?年.*?月.*?日)|(.*？月.*?日)"
    brand_regex = "(\".*?\")"
    law_entry = re.findall(law_regex,sentence)
    company_entry = re.findall(company_regex,sentence)
    time_entry = re.findall(time_regex,sentence)
    brand_entry = re.findall(brand_regex,sentence)
    entry_result = law_entry.__len__(),company_entry.__len__(),time_entry.__len__(),brand_entry.__len__()

    # print(tfidfs)
    max_similarity = sim_manualRule(sentence)
    tfidf = []
    for label,pair in tfidfs.items():
        sorted_tfidf = sorted(pair.items(),key = lambda  d:d[1],reverse = True)
        tmp_tfidf = get_largest_tag(words_only,sorted_tfidf)
        tfidf.append(tmp_tfidf[0])
    ### num of words, (law,company,time,brand),[[],,...,[]]
    # print(num)
    return num, str(entry_result)[1:-1],tfidf,max_similarity

### input : words: words of sentence(list)
###         sorted_tfidf: words, tfidf pair order by tfidf desc(list)
###         num : the num of output
### output: the index of words which have largest tfidf
def get_largest_tag(words, sorted_tfidf,num =4):
    result =[]
    for index in range(sorted_tfidf.__len__()):
        character = sorted_tfidf[index][0]
        if character in words:
            result.append(index+1)
        if result.__len__() == num:
            break
    while result.__len__()< num:
        result.append(0)
    return result

def get_largest_value(words, unsorted_tfidf,num =4):
    value = []
    for word in words:
        if word in unsorted_tfidf.keys():
            value.append(unsorted_tfidf[word])
    while value.__len__()<num:
        value.append(0.0)
    value = sorted(value)
    return value[0:num]

def analysis_single_sentences(sentence):
    pass



def demo_analysis():
    dir_classic = Dir.resourceDir+"已标注文书-txt/基础案例299篇-已标注/"
    print(dir_classic)
    data = dataloader.get_all_data(dir_classic)[1]
    save_dir = Dir.projectDir+"/analysis_result/"
    for label in data.keys():
        print(label)
        result = analsis_single_label_data(data[label])
        content =" num,average,noun_num,verb_num\n"
        content += str(result[:-1])+"\n"
        for i in range(result[-1].__len__()):
            content +=str(result[-1][i][0]+","+ str(result[-1][i][1]))+"\n"
        # for word in result[-1]:
        #     content += str(word)+","+str(result[-1][word])+"\n"
        if "/" in label:
            label= label.replace("/","-")
        save_file= save_dir+label+".txt"
        save_result(content,save_file)
### input:  a dict with labels as keys and its corresponding sentences as value(output of get_all'_data)
###         e.g. {"label":[sen1,..,senn],...,"labeln":[sen1,..,senn]}
def simple_data(data,save_path = Dir.resourceDir+"corpus/combine.txt"):
    result ={}
    save_content =""
    for name,content in data.items():
        labeled_content = dataloader.labeled_text(content)
        for sentences,label in labeled_content.items():
            if label.__len__() ==0:
                label = "0"
            else:
                label = "1"
            if label not in result:
                result[label]=[]
            sentences = sentences.strip()
            if sentences == "":
                continue
            result[label].append(sentences)
            save_content+= sentences+"\t"+label+"\n"
    Tools.saveIntoCsv(save_path,"sentence","tag")
    return result

### input: a file path which seperate by tab, contains 3 collums(label name    rule    order)
### ouput: a list([[labelname_1,rule_1,order_1],...,[labelname_n,rule_n,order_n]])
def load_manualRule(filepath =Dir.resourceDir+"人工模板.txt"):
    result =[]
    with open(filepath) as file:
        for line in file.readlines():
            tmp = line.split("\t")
            if tmp.__len__() == 3:
                result.append(tmp)
    return result

manual_rule=  load_manualRule()

### input: a list( load_manualRule's output, contains 3 collumns:label name rule    order)
### output: the max similarity value among all rules(if match with regex than the value will be 1)
def sim_manualRule(line, manual_rule = manual_rule):
    all_value=[]
    for rule in manual_rule:
        rule = rule[1]
        rule_regex = preprocess_data(rule)
        if re.findall(rule_regex,preprocess_data(line)).__len__()>0:
            all_value.append(1)
            continue
        all_value.append(similarity(line,rule))
    return max(all_value)

def remove_space(words):
    return [word for word in words if word.strip()!= '']

def similarity(sentence1,sentence2,preprocess=True):
    if preprocess:
        sentence1 = preprocess_data(sentence1)
        sentence2 = preprocess_data(sentence2)
    words1 = list(jieba.cut(sentence1))
    words2 = list(jieba.cut(sentence2))
    words1 = remove_space(words1)
    words2 = remove_space(words2)
    words_1,words_2 = words1,words2
    return normal_simi(words_1,words_2)

def normal_simi(words1,words2):
    tmp1 = set(words1)
    tmp2 = set(words2)
    inter = tmp1.intersection(tmp2)
    return (inter.__len__()+1)/(max([tmp1.__len__(),tmp2.__len__()])+1)

def demo_arff_simple(dir_classic,save_dir):
    print(dir_classic)
    tmp =dataloader.get_all_data(dir_classic)
    data = tmp[2]
    data2 = tmp[1]
    arff_title = ""
    for i in range(105):
        arff_title+= "attr"+str(i)+","
    arff_title+="class\n"
    arff_content =""
    count=0
    data2 = simple_data(data)
    tfidfs,possibile = build_tfidf(data2)
    for name in data.keys():
        print(count,"/",data.__len__())
        count+=1
        arff_content+=transfer2arff_simple(data[name],tfidfs)
    arff_content = arff_title+arff_content
    Tools.write(save_dir,arff_content)
    print("transfer completet, saved in:", save_dir)
dir_classic = Dir.resourceDir+"已标注文书-txt/典型案例111篇/"
save_dir = Dir.projectDir+"/result/arff_data_104_newregex_simple_maxsimi.csv"
demo_arff_simple(dir_classic,save_dir)
#
dir_classic = Dir.resourceDir+"已标注文书-txt/基础案例299篇-已标注/"
save_dir = Dir.projectDir+"/result/arff_data_299_newregex_simple_maxsimi.csv"
demo_arff_simple(dir_classic,save_dir)

dir_classic = Dir.resourceDir+"已标注文书-txt/all/"
save_dir = Dir.projectDir+"/result/arff_data_299+104_newregex_simple_maxsimi.csv"
demo_arff_simple(dir_classic,save_dir)

