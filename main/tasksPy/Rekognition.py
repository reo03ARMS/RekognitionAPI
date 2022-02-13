#ライブラリのインポート
from json.tool import main
import boto3
import configparser
from PIL import Image
import pandas as pd

#configparserのインスタンスを作る
ini = configparser.ConfigParser()
#あらかじめ作ったiniファイルを読み込む
ini.read("/home/ec2-user/config.ini", "UTF-8")

# 使用するバケットを指定する
bucket = "rekognitionsnaphy"
# 使用するリージョンを指定する
region = "us-east-1"

# サービスを利用するための識別情報(iniファイルの中身）を読み込む
access_key = ini["AWS_KEY"]["awsaccesskeyid"]
secret_key = ini["AWS_KEY"]["awssecretkey"]

# サービスへの接続情報を取得する
session = boto3.Session(
    aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region
)

# S3サービスに接続する
s3 = session.client("s3")
# Rekognitionサービスに接続する
rekognition = session.client("rekognition")


class RekognitionMain():
    #コンストラクタ
    def __init__(self,filename,id):
        # fileimg = Image.open(filename)
        self.filename = filename
        self.id = id
        print("id :" +self.id)
        
        
    
    #メソッド
    #写真データをAWSに送り戻り値は辞書型で返す
    def img_open(self):
        with open(self.filename, "rb") as f:
            # 読み込んだファイルをS3サービスにアップロード
            s3.put_object(Bucket=bucket, Key=self.filename, Body=f)
        # S3に置いたファイルをRekognitionに認識させる
        res = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": self.filename}}
        )
        keep_dict = {}
        for label in res["Labels"]:
            keep = {label["Name"]:label["Confidence"]}
            keep_dict.update(keep)
        
        return keep_dict
    
    #データフレームの作成
    def create_dataflame(self,keep_dict):
        
        df = pd.DataFrame.from_dict(keep_dict,orient='index').rename(columns={0:self.id})
        #csv 保存
        df.to_csv("sample01.csv",na_rep=0)
        
        
    #AWSサーバからログアウト
    def logout(self):
        # S3サービスにアップロードしたファイルを削除する
        s3.delete_object(Bucket=bucket, Key=self.filename)
        


#新規データを既存にデータフレームにcsvで保存
class dataframe():
    #コンストラクタ
    def __init__(self,keep_dict,img_path):
        try:
            df = pd.read_csv('sample01.csv',header=0,index_col=0)
            self.df = df.T
        except:
            df = pd.DataFrame.from_dict(keep_dict,orient='index').rename(columns={0:img_path})
            #csv 保存
            df.to_csv("sample01.csv",na_rep=0)
            
            self.df = df
        self.keep_dict = keep_dict
            
        
    #メソッド
    #データを追加
    def add_df(self,sub_fileName):
        columns_list = self.df.columns.tolist()

        if sub_fileName in columns_list:
            print("既にデータがあります")
            
            #ーーーー1回目ーーーーー
            # self.df = self.df.T
            # #csv 保存
            # self.df.to_csv("sample01.csv",na_rep=0)
            #--------------------
        else:
            add_df = pd.DataFrame.from_dict(self.keep_dict,orient='index').rename(columns={0:sub_fileName})
        
            # 新規データを横に連結
            df = pd.concat([self.df, add_df], axis=1)
            
            #縦を横にして保存
            df = df.T
            
             #csv 保存
            df.to_csv("sample01.csv",na_rep=0)
            
            sub_df = pd.read_csv('sample01.csv', header=0,index_col=0)
            print(sub_df)
    

        
if __name__ == "__main__":
    img_path = "Images/0.jpg"
    test = RekognitionMain(img_path)#解析したい写真のPath
    keep_dict = test.img_open()
    test.logout()
    test2 = dataframe(keep_dict,test.id)
    test2.add_df(test.id)

    
