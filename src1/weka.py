__author__ = 'E440'
import Dir
from nltk.internals import java, config_java
import subprocess
from sys import stdin
import re

### weka cmd:
### java weka.classifiers.trees.J48 -p 9 -l directory-path\bank.model -T directory-path \bank-new.arff
weka_class_path = Dir.projectDir+"/resources/weka3-6-6.jar"
class WekaClassifier():
    def __init__(self):
        config_java()
    def weka_classify(self,arff_file,model_file):
        class_index=1
        with open(arff_file,mode="r",encoding="utf-8") as file:
            lines = file.readlines()
            for i in range(lines.__len__()):
                if "@attribute class" in lines[i]:
                    class_index = i
                    break
        cmd =["weka.classifiers.trees.RandomForest","-p",str(class_index),"-l",str(model_file),"-T",str(arff_file)]
        (stdout, stderr)  = java(cmd, classpath=weka_class_path,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result= stdout.decode(stdin.encoding)
        result = result[result.index("prediction ()")+"prediction ()".__len__():].strip()
        tmp = result.split("\n")
        final_result =[re.split(" +",t.strip()) for t in tmp]
        # for res in final_result:
        #     print(res)
        return  final_result

if __name__ == "__main__":
    weka = WekaClassifier()
    arff_file = Dir.projectDir+"/src1_result/arff_new/data_111_two.arff"
    model_file = Dir.projectDir+"/src1_result/arff_result/model/data111_randomforest.model"
    weka.weka_classify(arff_file,model_file)


