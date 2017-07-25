import win32com.client as client
import Dir
import Tools as tools

def word2txt(word_file,save_file = Dir.projectDir+"/Tmp/word2txt/"):
    wordapp = client.gencache.EnsureDispatch("Word.Application")
    print(word_file)
    save_file += tools.get_filename(word_file)+".txt"
    print(save_file)
    wordapp.Documents.Open(word_file)
    # 修改成txt文件名  word_file[:-3]表示取从开始到倒数第三个字符


    # 转换成txt文件
    wordapp.ActiveDocument.SaveAs(save_file, FileFormat=client.constants.wdFormatText)
    wordapp.ActiveDocument.Close()

def word2txt_batch(word_dir,save_dir):
    filelist=tools.get_all_files(word_dir)
    for file in filelist:
        word2txt(file,save_dir)


dir = Dir.projectDir+"/data/test.docx"
word2txt(dir)

