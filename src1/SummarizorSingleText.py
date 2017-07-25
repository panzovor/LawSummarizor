import src1.weka as weka_model
import src1.extract_sentence as extractor
import src1.short_sentence_feature_generator as feature_generator
import Dir
import src1.DataLoader as dataLoader

file_pat = Dir.projectDir+"/Tmp/result.txt"

def order_sentences(text,sentences):
    result=[]
    final_result = []
    text = dataLoader.pre_process(text)
    tmp ={}
    for sentence,label in sentences:
        tmp[sentence] = label
        result.append([sentence,text.index(sentence)])
    result = sorted(result,key = lambda d:d[1])
    for sen,index in result:
        final_result.append([sen,tmp[sen]])
    return final_result

default_parameter={
                   False:[Dir.projectDir+"/src1_result/model/short_sentence_feature_model_data_all_multi.model",
                         Dir.projectDir + "/src1_result/arff_result/model/dataall_randomforest_new_multi.model" ],
                   True:[Dir.projectDir+"/src1_result/model/short_sentence_feature_model_data_all_two.model",
                         Dir.projectDir + "/src1_result/arff_result/model/dataall_randomforest_new_two.model" ]
                   }

def summarize(text,paragraph=False,two_class = False):
    feature_generator_model = default_parameter[two_class][0]
    weka_model_path = default_parameter[two_class][1]

    if paragraph:
        feature_generator_model =Dir.projectDir+"/src1_result/model/short_sentence_feature_model_data_labeled_two.model"
        weka_model_path =Dir.projectDir + "/src1_result/arff_result/model/dataParagraph_randomforest.model"

    sentences = extractor.extract_setence(text,two_class=two_class, paragraph=  paragraph)
    model = feature_generator.load_model(feature_generator_model)
    result= []
    result.append(model[4])
    sentences = sorted(sentences)
    for sentence in sentences:
        # print(sentence.strip(),sentences.index(sentence))
        label = sentence.split("\t")[1].strip()
        feature = feature_generator.feature_single_sentence(model,sentence,real_label=label)
        result.append(feature)
    arff_path_tmp = Dir.projectDir+"/Tmp/arfffile.arff"
    feature_generator.conver2arfffile(result,arff_path_tmp)
    result =weka_model.weka_classify(arff_path_tmp,weka_model_path)
    result_sentences = []
    label_index = {}
    for label,index in model[3].items():
        label_index[index] = label
    for key in result.keys():
        if two_class:
            if int(result[key][0]) !=model[3]["0"] :
                result_sentences.append([sentences[int(key)-1].split("\t")[0].strip(),label_index[int(result[key][0])]])
        if not two_class:
            if int(result[key][0]) != model[3]["null"]:
                result_sentences.append([sentences[int(key) - 1].split("\t")[0].strip(),label_index[int(result[key][0])]])
    return order_sentences(text,result_sentences)

if __name__ == "__main__":
    test_path = Dir.projectDir+"/data/已标注文书-txt/all/(2007)鲁民三终字第105号.txt"
    content =""
    with open(test_path,mode="r",encoding="utf-8") as file:
        content = file.read()
    sens = summarize(content,True,False)
    for sen in sens:
        print(sen)
    print(sens.__len__())