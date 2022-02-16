from asyncio import futures
import main.tasksPy.firebaseAcsess as firebaseAcsess
import main.tasksPy.Rekognition as Rekognition
from concurrent.futures.thread import ThreadPoolExecutor

        
def main(a,b):
    print("start :" + a)
    search = Rekognition.RekognitionMain(a,b)
    keep_dict = search.img_open()
    search.logout()
    test2 = Rekognition.dataframe(keep_dict,a)
    test2.add_df(search.id)
    print("stop :" + a)
    return b
        
def heiretu():

    imgURL_list,doc_id_list = firebaseAcsess.ConnectFirebase().ClothesImageURLGet()
    features = []
    with ThreadPoolExecutor() as executor:
        for i in range(len(imgURL_list)):
            features = [executor.submit(main,imgURL_list[i],doc_id_list[i])]
        for feature in features:
            print(feature.result())
    
        
if __name__ == "__main__":
    # main()
    a = heiretu()
    print(a)
    