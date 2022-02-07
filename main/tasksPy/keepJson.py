import json

class keepJson():
    def __init__(self,id,imgURL) :
        self.id = id
        self.data = {id:{"imgURL":imgURL}}
        self.filename = "main/tasksPy/Images/localData.json"
        
    def appdateJson(self):
        with open(self.filename,"r") as j_w:
            read_data = json.load(j_w)
        read_data.update(self.data)
        with open(self.filename, 'w') as f:
            json.dump(read_data, f,indent=2)
        
    def serchJson(self):
        json_open = open(self.filename, 'r')
        json_load = json.load(json_open)
        if(self.id in json_load):
            return True
        else:
            return False
        
    
    def readJson(self):
        with open(self.filename,"r") as j_r:
            j_show=json.load(j_r)
        print(j_show)

if __name__ == "__main__":
    a = keepJson("i5QirBZf0aaJcG2uESJg","test")
    a.serchJson()
    # a.appdateJson()
    # a.readJson()