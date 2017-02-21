import jieba.posseg as posseg
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
import Dir

### input : filename ,enconding = utf-8
###         e.g. sentence1\tlabel\n
###              sentence2\tlabel2\n
### output: a dict
###         e.g. {'label':[sentence1,...,sentencen],...,'label_n':{sentence1,...,sentencen}
def read(filename):
    data = {}
    with open(filename,mode="r") as file:
        for line in file.readlines():
            line = line.strip()
            tmp = line.split("\t")
            if tmp.__len__() == 2:
                if tmp[1] not in data.keys():
                    data[tmp[1]] =[]
                data[tmp[1]].append(tmp[0])
            else:
                string = ''.join(tmp[:-1])
                if tmp[-1] not in data.keys():
                    data[tmp[-1]] = []
                data[tmp[-1]].append(string)
    return data

### input : output from read
###        e.g. {'label': [sentence1, ..., sentencen], ..., 'label_n':{sentence1, ..., sentencen}
###         tfidf_num : pick the largest n tfidf value
###         words_poss_num : if 0 than contain all value order by words appeareace
###                          if >0 than output each label's largest n words_possiblity and avg of all word_possiblity
### output: feature's title and feature of sentences,including(num of noun,num of verb,num of sepicial,label's tfidf(sorted), possible of words,possible of label)
###        e.g. num_noun,num_verb, num_sepecial,label1-1,label-2,label2-1,label2-2,word1-poss,words2-poss,words3-poss,label1-poss,label2-poss
###             {sentence: [2,1,3,  0.3,0.2, 0.4,0.2,  0.001,0.023,0.55  ,0.4,0.6] }
###                            |      |                       |              |
###                   num feature  tfidf_feature   word_poss_feature     label_poss_feature
###
def feature_generator(data):
    label_index = {}
    tfidf_corpus = []
    counter =0
    words_label_count ={}
    model = []
    ### num features
    for label,label_data in data.items():
        label_index[label] = counter
        counter+=1
        words_each_label = []
        for sentence in label_data:
            words_tag = posseg.cut(sentence)
            for word, tag in words_tag:
                words_each_label.append(word)
                if word not in words_label_count.keys():
                    words_label_count[word] = {}
                if label not in words_label_count[word].keys():
                    words_label_count[word][label] = 0
                words_label_count[word][label] += 1
        tfidf_corpus.append(' '.join(words_each_label))
    ### label_poss_feature
    label_poss_feature = []
    for label in label_index.keys():
        label_poss_feature.append(data[label].__len__())
        words_each_label = []

    data_count = sum(label_poss_feature)
    label_poss_feature = [ var/data_count for var in label_poss_feature]
    model .append(label_poss_feature)

    ### tfidf features
    tfidf_dict = tfidf(tfidf_corpus)
    model.append(tfidf_dict)

    ### word_poss_feature
    word_poss_feature = {}



    for word,label_count in words_label_count.items():
        word_poss_feature[word] = []
        label_count = sum(words_label_count[word].values())
        for label in label_index.keys():
            if label not in words_label_count[word].keys():
                words_label_count[word][label] = 0
            word_poss_feature[word].append(words_label_count[word][label]/label_count)

    model.append(word_poss_feature)
    model.append(label_index)

    feature_title = "num_noun,num_verb,"
    return model


### input : output from read
###        e.g. {'lable': [sentence1, ..., sentencen], ..., 'label_n':{sentence1, ..., sentencen}
###         tfidf_num : pick the largest n tfidf value
###         words_poss_num : if 0 than contain all value order by words appeareace
###                          if >0 than output each label's largest n words_possiblity and avg of all word_possiblity
### output: feature's title and feature of sentences,including(num of noun,num of verb,num of sepicial,label's tfidf(sorted), possible of words,possible of label)
###        e.g. num_noun,num_verb, num_sepecial,label1-1,label-2,label2-1,label2-2,word1-poss,words2-poss,words3-poss,label1-poss,label2-poss
###             {sentence: [2,1,3,  0.3,0.2, 0.4,0.2,  0.001,0.023,0.55  ,0.4,0.6] }
###                            |      |                       |              |
###                   num feature  tfidf_feature   word_poss_feature     label_poss_feature
###
def feature_generator_bak(data,tfidf_num = 4,word_poss_num =4):
    label_index = {}
    tfidf_corpus = []
    sentences_features= {}
    counter =0
    words_label_count ={}
    model = []
    ### num features
    for label,label_data in data.items():
        label_index[label] = counter
        counter += 1
        words_each_label = []
        for sentence in label_data:
            words_tag = posseg.cut(sentence)
            num_noun, num_verb = 0, 0
            for word, tag in words_tag:
                if "n" in tag:
                    num_noun+=1
                elif "v" in tag:
                    num_verb+=1
                words_each_label.append(word)
                if word not in words_label_count.keys():
                    words_label_count[word] = {}
                if label not in words_label_count[word].keys():
                    words_label_count[word][label] = 0
                words_label_count[word][label]+=1
            sentences_features[sentence] =[num_noun,num_verb]
        tfidf_corpus.append(' '.join(words_each_label))
    ### label_poss_feature
    label_poss_feature = []
    for label in label_index.keys():
        label_poss_feature.append(data[label].__len__())
    data_count = sum(label_poss_feature)
    label_poss_feature = [ var/data_count for var in label_poss_feature]
    model .append(label_poss_feature)

    ### tfidf features
    tfidf_dict = tfidf(tfidf_corpus)

    model.append(tfidf_dict)

    for label in label_index:
        used_sentence = set()
        for sentence in data[label]:
            if sentence not in used_sentence:
                used_sentence.add(sentence)

                sentence_tfidf_matrix=[]
                for word,tag in posseg.cut(sentence):
                    sentence_tfidf_matrix.append(tfidf_dict[word])
                sentence_tfidf_matrix = transposition_sortedrow(sentence_tfidf_matrix)

                for line in sentence_tfidf_matrix:
                    while line.__len__() <= tfidf_num:
                        line.append(0.0)
                    line = line [0:tfidf_num]
                    sentences_features[sentence].append(line)

                # pass
    ### word_poss_feature
    word_poss_feature = {}
    model.append(word_poss_feature)
    model.append(label_index)

    for word,label_count in words_label_count.items():
        word_poss_feature[word] = []
        label_count = sum(words_label_count[word].values())
        for label in label_index.keys():
            if label not in words_label_count[word].keys():
                words_label_count[word][label] = 0
            word_poss_feature[word].append(words_label_count[word][label]/label_count)
    if word_poss_num <= 0:

        for label in label_index:
            for sentence in data[label]:
                tmp =[]
                for word, words_tag in posseg.cut(sentence):
                    tmp.append( word_poss_feature[word])
                tmp = sorted(tmp,reverse=True)
                if label_poss_feature not in sentences_features[sentence]:
                    sentences_features[sentence].append(tmp)
                    sentences_features[sentence].append(label_poss_feature)
    else:
        for sentence in sentences_features.keys():
            word_poss_matrix = []
            for word,words_tag in posseg.cut(sentence):
                tmp =[]
                for label in label_index:
                    tmp.append(word_poss_feature[word][label_index[label]])
                word_poss_matrix.append(tmp)
            word_poss_matrix = transposition_sortedrow(word_poss_matrix)
            for line in word_poss_matrix:
                line_avg = sum(line)/line.__len__()
                if line.__len__()<word_poss_num:
                    while (line.__len__() <=word_poss_num):
                        line.append(0.0)
                line_tmp =line[0:word_poss_num]
                line_tmp.append(line_avg)
                sentences_features[sentence].append(line_tmp)
            sentences_features[sentence].append(label_poss_feature)


    ### class
    for label, label_data in data.items():
        used_sentence = set()
        for sentence in label_data:
            if sentence not in used_sentence:
                sentences_features[sentence].append(str(label))
                used_sentence.add(sentence)

    feature_title = "num_noun,num_verb,"
    return feature_title, label_index,sentences_features,model

### input: model        : generate by feature_generator
###        sentence     : a string sentence
###        real_label   : label of sentence, default value is '0'
###        tfidf_num    : num of tfidf value of each label
###        word_poss_num: if 0 than contain all value order by words appeareace
###                       if >0 than output each label's largest n words_possiblity and avg of all word_possiblity
### output: feature's title and feature of sentences,including(num of noun,num of verb,num of sepicial,label's tfidf(sorted), possible of words,possible of label)
###        e.g. num_noun,num_verb, num_sepecial,label1-1,label-2,label2-1,label2-2,word1-poss,words2-poss,words3-poss,label1-poss,label2-poss
###             {sentence: [2,1,3,  0.3,0.2, 0.4,0.2,  0.001,0.023,0.55  ,0.4,0.6] }
###                            |      |                       |              |
###                   num feature  tfidf_feature   word_poss_feature     label_poss_feature
###
def feature_single_sentence(model,sentence,real_label='0',tfidf_num=4,word_poss_num = 4):
    words_tag = list(posseg.cut(sentence))
    num_noun, num_verb = 0, 0
    features = []

    ### num_features
    for word, tag in words_tag:
        if "n" in tag:
            num_noun += 1
        elif "v" in tag:
            num_verb += 1
    features.extend([num_noun, num_verb])

    ### sepecial regex
    time_regex = "(.{1,4}年.{1,2}月.{1,2}日)|(.{1,2}月.{1,2}日)"
    law_regex = "(《.*?》)"
    sepecial_num = 0
    time_num = re.findall(time_regex, sentence).__len__()
    law_num = re.findall(law_regex, sentence).__len__()
    if time_num > 0:
        sepecial_num+=time_num
    if law_num>0:
        sepecial_num+=law_num

    ### label_poss_feature
    label_poss_feature = model[0]

    ### tfidf_features
    tfidf_dict = model[1]
    label_index = model[3]

    features.append(sepecial_num)


    sentence_tfidf_matrix = []
    for word, tag in words_tag:
        # sentence_tfidf_matrix.append(tfidf_dict[word])
        if word in tfidf_dict.keys():
            sentence_tfidf_matrix.append(tfidf_dict[word])
        else:
            sentence_tfidf_matrix.append(np.zeros(label_index.__len__()))
    sentence_tfidf_matrix = transposition_sortedrow(sentence_tfidf_matrix)
    for line in sentence_tfidf_matrix:
        while line.__len__() <= tfidf_num:
            line.append(0.0)
        line = line[0:tfidf_num]
        features.extend(line)

    ### word_poss_feature
    word_poss_feature = model[2]
    # label_index = model[3]
    if word_poss_num <= 0:
        tmp = []
        for word, tag in words_tag:
            tmp.append(word_poss_feature[word])
        tmp = sorted(tmp, reverse=True)
        features.extend(tmp)
    else:
        word_poss_matrix = []
        for word, tag in words_tag:
            tmp = []
            for label in label_index:
                tmp.append(word_poss_feature[word][label_index[label]])
            word_poss_matrix.append(tmp)
        word_poss_matrix = transposition_sortedrow(word_poss_matrix)
        for line in word_poss_matrix:
            line_avg = sum(line) / line.__len__()
            if line.__len__() < word_poss_num:
                while (line.__len__() <= word_poss_num):
                    line.append(0.0)
            line_tmp = line[0:word_poss_num]
            line_tmp.append(line_avg)
            features.extend(line_tmp)

    ### label_poss_feature
        features.extend(label_poss_feature)

    ### class
        features.append(real_label)
    return features


def tfidf(corpus):
    result = {}
    # corpus = ["我 来到 北京 清华大学",  # 第一类文本切词后的结果，词之间以空格隔开
    #           "他 来到 了 网易 杭研 大厦",  # 第二类文本的切词结果
    #           "小明 硕士 毕业 与 中国 科学院",  # 第三类文本的切词结果
    #           "我 爱 北京 天安门"]  # 第四类文本的切词结果
    vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b")  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for j in range(len(word)):
        for i in range(len(weight)):
            if word[j] not in result.keys():
                result[word[j]] =[]
            result[word[j]].append(weight[i][j])
    return result

def transposition_sortedrow(a,reverse = True):
    a = list(map(list,zip(*a)))
    for index in range(a.__len__()):
        a[index] = sorted(a[index],reverse = reverse)
    return a

def save_model(model,savepath):
    ### label_poss_feature
    ### e.g. [0.1, 0.3 ]
    label_poss_feature = model[0]

    ### tfidf_features
    ### tfidf
    ### e.g.  word: [0.1,  0.2, 0.3]
    tfidf_dict = model[1]

    ### word_poss_feature
    ### e.g.  word-label-value
    word_poss_feature = model[2]

    ### label_index
    ### e.g.  {"label":index}
    label_index = model[3]

    seperater= "\n###seperate###\n"
    detail_sepeate = "\t"
    sepecial_replace_words = "tab_#"
    content = str(label_poss_feature)[1:-1]

    content+= seperater
    for word in tfidf_dict.keys():
        tmp = word
        if word == detail_sepeate:
            tmp = sepecial_replace_words
        content+=tmp+detail_sepeate+str(tfidf_dict[word])[1:-1]+"\n"
    content = content[:-1]
    content+= seperater
    for word in word_poss_feature.keys():
        tmp = word
        if word == detail_sepeate:
            tmp = sepecial_replace_words
        content += tmp+detail_sepeate+str(word_poss_feature[word])[1:-1]+"\n"
    content = content[:-1]
    content+= seperater
    for label,index in label_index.items():
        content+=label+detail_sepeate+str(index)+"\n"


    with open(savepath,mode="w") as file:
        file.write(content)


def load_model(modelpath):
    model =[]
    with open(modelpath,mode="r") as file:
        content = file.read()
    seperater = "\n###seperate###\n"
    detail_sepeate= "\t"
    sepecial_replace_words = "tab_#"
    if seperater in content:
        tmp  =content.split(seperater)
        if tmp.__len__() == 4:
            label_poss_feature = [float(var) for var in tmp[0].split(",")]
            model.append(label_poss_feature)

            tfidf_features = {}
            for line in tmp[1].split("\n"):
                if detail_sepeate in line:
                    tfidf_tmp = line.split(detail_sepeate)
                    if "," in tfidf_tmp[1]:
                        if tfidf_tmp[0]== sepecial_replace_words:
                            tfidf_tmp[0] = "\t"
                        tfidf_features[tfidf_tmp[0]]= [float(var) for var in tfidf_tmp[1].split(",")]
            model.append(tfidf_features)

            word_poss_feature = {}
            for line in tmp[2].split("\n"):
                if detail_sepeate in line:
                    word_poss_tmp = line.split(detail_sepeate)
                    if "," in word_poss_tmp[1]:
                        if word_poss_tmp[0] ==sepecial_replace_words:
                            word_poss_tmp[0] ="\t"
                        word_poss_feature[word_poss_tmp[0]] = [float(var) for var in word_poss_tmp[1].split(",")]
            model.append(word_poss_feature)

            label_index = {}
            if "\n" in tmp[3]:
                label_tmp = tmp[3].split("\n")
                for line in label_tmp:
                    if detail_sepeate in line:
                        label_index_tmp  = line.split(detail_sepeate)
                        label_index[label_index_tmp[0]] = int(label_index_tmp[1])
            model.append(label_index)

        return model
    else:
        print("model format damaged")
        return None

def convert(filepath,savepath):
    content = "@relation train_file\n"
    with open(filepath,mode="r",encoding="utf-8") as file:
        lines = file.readlines()
        data_content =""
        class_label =set()
        for i in range(lines.__len__()):
            if i  == 0:
                tmp = lines[0].split(",")
                for j in range(tmp.__len__()-1):
                    tmp_string = tmp[j]
                    content+= "@attribute "+tmp_string+" numeric\n"

            # else:
            #     data_content+=str(lines[i])[:-1]+"\n"
            label = lines[i].split(",")[-1].strip()
            if label !="class":
                class_label.add(label)
        # for i in range(1,lines.__len__()):
        #     print(i)
        #     data_content+=lines[i]+'\n'
        sorted(class_label)
        # print(class_label)
        content += "@attribute class {"
        for label in class_label:
            content+=label+","
        content = content[:-1]
        content+="}\n@data \n"
        # content+=data_content
    with open(filepath, mode="r", encoding="utf-8") as file:
        file_content = file.read()
        real_content = file_content.split("\n",1)[1]
        content+=real_content

    with open(savepath,mode="w",encoding="utf-8") as file:
        file.write(content)

def demo(dataname):
    # dataname ="data_111_two"
    filename = Dir.projectDir+"/src1_result/new_extract_data/"+dataname
    data =read(filename)
    # print(sum([var.__len__() for var in data.values()]))
    model = feature_generator(data)
    savepath =  Dir.projectDir+"/src1_result/model/short_sentence_feature_model_"+dataname+".model"

    save_model(model,savepath)
    model1 = load_model(savepath)
    feature = []
    tmp = model[-1]
    title = "num_noun,num_verb,sepecial_num,"
    num_tfidf = 4
    word_poss_num = 4
    label_sorted = list(sorted(tmp.items(), key=lambda d: d[1]))
    for i in range(label_sorted.__len__()):
        for j in range(num_tfidf):
            title += label_sorted[i][0] + "-tfidf-" + str(j) + ","
    for i in range(label_sorted.__len__()):
        for j in range(word_poss_num):
            title += label_sorted[i][0] + "-wp-" + str(j) + ","
        title += label_sorted[i][0] + "-avg,"
    for i in range(label_sorted.__len__()):
        title+= "label_poss_"+str(label_sorted[i][0])+","
    title += "class\n"
    print(title)

    feature.append(title)
    for label in data.keys():
        for sen in data[label]:
            string = feature_single_sentence(model1,sen,label,num_tfidf,word_poss_num)
            feature.append(str(string)[1:-1]+"\n")
    print(feature.__len__())
    filepath = Dir.projectDir+"/src1_result/csv/"+dataname+".csv"
    with open(filepath,mode="w",encoding="utf-8") as file:
        file.writelines(feature)
        file.flush()
    filepatha_rff = Dir.projectDir+"/src1_result/arff_new/"+dataname+".arff"
    convert(filepath,filepatha_rff)
    print(dataname,"done")

datanames = ['data_111_two','data_111_multi','data_299_two','data_299_multi','data_all_two','data_all_multi']
data_multi = ['data_111_multi','data_299_multi','data_all_multi']
data_two = ['data_111_two','data_299_two','data_all_two']
# for name in data_two:
#     demo(name)
demo("data_labeled_two")

