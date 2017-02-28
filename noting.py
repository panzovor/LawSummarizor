# __author__ = 'E440'
# import re
# # ### encode = 'UTF-8'
# #
# # dict1 = {"c":3,"b":5,"a":1,"b":2}
# # dict2 = {"c":3,"b":5}
# #
# # dict3 = dict(sorted(dict1.items(), key = lambda d: d[0],reverse = True))
# # print(dict3)
# # print(type(dict3))
# #
# # import jieba.posseg as pg
# #
# # string ='我爱北京天安门'
# # word= list(pg.cut(string))
# # print(type(word))
# # print(word.__len__())
# # for wor, pog in word:
# #     print(wor,pog)
#
# strings = ['a','b','c','']
# strings.remove('')
# print(strings)
#
#
# example = {'a':{'dd':10,"cc":1222},'b':{'aa':123,'cd':32}}
# example_ = example.copy()
# for name,value in example.items():
#     if name == 'a':
#         example[name] = []
# print(example)
# print(example_)
#
#
# import re
# string = "我爱\"北京\"天安门"
# brand_regex = "((\").*?\")"
# result = re.findall(brand_regex,string)
# print(result.__len__())
#
# example_ = {"d":1,"c" :3,"a":2}
# example_ = sorted(example_.items(),key = lambda  d:d[1],reverse = True)
# print(example_)
#
#
# example_ = [[1,2],[2,1]]
#
# string = "####"
# string = string.replace("#+","")
# print(string)
# import re
# string = re.sub("#+","#",string)
# print(string)
#
#
# import numpy as np
#
# print(np.zeros(6))
#
#
# import jieba
# def preprocess_data(sentence):
#     time_regex = "(.{1,4}年.{1,2}月.{1,2}日)|(.{1,2}月.{1,2}日)"
#     law_regex = "(《.*?》)"
#     x_regex = "\*+|\".*?\""
#     sentence_ = re.sub(time_regex, " 时间 ", sentence)
#     sentence_ = re.sub(law_regex, " 法律 ", sentence_)
#     sentence_ = re.sub(x_regex, "实体", sentence_)
#     return sentence_
#
# def remove_space(words):
#     return [word for word in words if word.strip()!= '']
#
# # string = "著作权归属	20**年*月*日，由***设计的\"****\"作品，系20**年*月*日，***委托***进行***设计时产生的美术作品。根据合同约定，\"****\"作品权属归***所有，即该\"****\"作品著作权属于***。	12"
# # string = preprocess_data(string)
# # print(string)
# # wordss = remove_space(list(jieba.cut(string)))
# # print(wordss)
# # string1 = ''.join(wordss)
# # print(string1)
# # print(list(jieba.cut(string1)))
# # rule_regex = preprocess_data(string)
# # print(rule_regex)
# # rule_regex = rule_regex.replace("实体",".*?")
# # rule_regex = rule_regex.replace("时间",".*?")
# # print(rule_regex)
#
# def transposition_sortedrow(a,reverse = True):
#     a = list(map(list,zip(*a)))
#     for index in range(a.__len__()):
#         a[index] = sorted(a[index],reverse = reverse)
#     return a
#
# a=[[1, 2, 3], [7, 8, 9], [4, 5, 6], [10, 11, 12]]
# a = {1:1,2:23,3:4}
# #
# # a = sorted(a.items(), key = lambda d:d[1])
# # for res in a:
# #     print(resd)
# # # print(a[0][0])
# #
# # print("===============")
# #
# # def pre_process(string):
# #     regex = "：(?:.*?；)+"
# #     seperate = re.findall(regex,string)
# #     value = re.split(regex,string)
# #     string_result = ""
# #     if value.__len__()>1 and  seperate.__len__()==  value.__len__()-1:
# #         for i in range(value.__len__()):
# #             string_result+= value[i]
# #             if i < value.__len__()-1:
# #                 string_result+= seperate[i].replace("；","@")
# #     else:
# #         string_result=string
# #     return string_result
# #
# # filepath="G:\Czb\国双课题\workspace\Summarizor\src1_result\csv\data_111_multi.txt.csv"
# # with open(filepath, mode="r", encoding="utf-8") as file:
# #     file_content = file.read()
# #     real_content = file_content.split("\n", 1)[1]
# #     print(real_content)
# #
#
# # filepath ="D:\workspace\LawSummarizor\data\已标注文书-txt\paragraph_labeled\\3-宜宾五粮液股份有限公司与北京谭氏瑞丰商贸有限公司侵害商标权纠纷一案二审民事判决书.txt"
# # regex= "<.*?商标知名度.*?>(.|\\n*?)</.*?商标知名度.*?>"
# # with open(filepath,mode="r",encoding="utf-8") as file:
# #     content = file.read()
# # result = re.findall(regex,content)
# # import src1.DataLoader as loader
# # result = loader.labeled_text(content)
# # for sen,label in result.items():
# #     if isinstance(label,str):
# #         print(label,sen)
#
#
# string ="aaaaab"
# print(string[:-1])
#
# brand_regex="院.{0, 4}认为"
# import re
# res = re.findall(brand_regex,string)
# print(res)


# def filter(content):
#     names = ['原告经营情况','企业名称变更','注册商标权利情况','证明商标使用管理规则','商标许可/转让情况','商标共有情况','商标知名度','驰名商标','申请驰名商标司法认定','证据保全公证','著作权登记','著作权归属','被告经营情况','行为人商标使用情况','与域名相关的事实','贴牌加工行为','合法来源','未实际使用','商标行政程序','商标权行政诉讼','商标权行政处罚','商标权犯罪']
#     names.extend(['合理开支','产品利润','违法收入','原产地域名称情况'])
#     regex = ""
#     for name in names:
#         regex+="</{0,1}"+name+">|"
#     regex = regex[:-1]
#     print(regex)
#
# filter("dd")
#
#


for i in range(1,10):
    print(i)

def twoSum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    small_num = [var for var in nums if var<= target/2]
    big_num = [var for var in nums if var>target/2 and var <target]
    print(small_num,big_num)
    for small in small_num:
        for big in big_num:
            if small+big == target:
                return [nums.index(small),nums.index(big)]
    return None

result =twoSum([3,2,4],6)
print(result)