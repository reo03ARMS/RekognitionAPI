import RekognitionAPI.main.tasksPy.firebaseAcsess as firebaseAcsess
import RekognitionAPI.main.tasksPy.Rekognition as Rekognition



def main():
    imgURL_list,doc_id_list = firebaseAcsess.ConnectFirebase().ClothesImageURLGet()
    for i in range(len(imgURL_list)):
        search = Rekognition.RekognitionMain(imgURL_list[i],doc_id_list[i])
        keep_dict = search.img_open()
        search.logout()
        test2 = Rekognition.dataframe(keep_dict,imgURL_list[i])
        test2.add_df(search.id)
        i += 1
        
if __name__ == "__main__":
    main()