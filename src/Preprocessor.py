import src.DataLoader as DataLoader
import Dir

def preprocess(labeled_dir,save_path):
    data = DataLoader.get_all_data(labeled_dir)[2]
    result ={}
    for name,content in data.items():
        labeled_content = DataLoader.labeled_text(content)
        for sentences,label in labeled_content.items():
            if label.__len__() ==0:
                label = "0"
            else:
                label = 1
            if label not in result:
                result[label]=[]
            result[label].append(sentences)
    return result

