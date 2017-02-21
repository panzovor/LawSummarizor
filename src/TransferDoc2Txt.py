__author__ = 'E440'
from win32com import client as wc

def transfer(doc_file, txt_file):
    word = wc.Dispatch('Word.Application')
    doc = word.Documents.Open(doc_file)
    doc.SaveAs(txt_file, 4)
    doc.Close()
    word.Quit()

def transfer_all():
    import Dir
    import Tools
    classic_dir = Dir.resourceDir+"原文书-word/典型案例库111篇/"
    classic_file_list = []
    Tools.get_filelist(classic_dir,classic_file_list)
    basic_dir = Dir.resourceDir+"原文书-word/基础文书库299篇/"
    basic_file_list = []
    Tools.get_filelist(basic_dir,basic_file_list)

    classic_save_dir=  Dir.resourceDir+"原文书-txt/典型案例库111篇/"
    basic_save_dir=  Dir.resourceDir+"原文书-txt/基础文书库299篇/"
    for filename in classic_file_list:
        savename = classic_save_dir+Tools.get_filename(filename)[:-5]+".txt"
        transfer(filename,savename)
    for filename in basic_file_list:
        savename = basic_save_dir+Tools.get_filename(filename)[:-5]+".txt"
        transfer(filename,savename)


transfer_all()