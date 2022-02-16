import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import urllib.error
import urllib.request
import main.tasksPy.keepJson as keepJson
import os


def download_file(url,count):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            dst_path= "main/tasksPy/Images/"+str(count)+".jpg"
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
                return dst_path
    except urllib.error.URLError as e:
        print(e)


class ConnectFirebase():
    def __init__(self):
        if not firebase_admin._apps:
            # 初期済みでない場合は初期化処理を行う
            # cred = credentials.Certificate("/home/ec2-user/ServisAcoountKey.json")
            cred = credentials.Certificate('../AcoountKey.json') #ローカル
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()


    def ClothesImageURLGet(self):
        docs = self.db.collection(u'Images').stream()
        imgURL_List = []
        doc_id_list = []
        count = 0
        for doc in docs:
            val = doc.to_dict()
            doc_id = doc.id
            
            #既にデータが存在するかのチェック
            check = keepJson.keepJson(doc_id,val["imgURL"])
            if (check.serchJson() == True):
                print("既にデータが存在しています")
            else:
                check.appdateJson()
                clothe_images = val["imgURL"]
                clothe_image = download_file(clothe_images,count)
                imgURL_List.append(clothe_image)
                doc_id_list.append(doc_id)
                count += 1
        return imgURL_List,doc_id_list

if __name__ == "__main__":
    a = ConnectFirebase().ClothesImageURLGet()
    print(a)
