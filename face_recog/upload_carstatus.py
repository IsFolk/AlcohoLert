# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import GeoPoint
import json

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('./serviceAccount.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()



def getindex():
    file = open("Index.json", "r")
    data = json.load(file)
    file.close()
    return data["Index"]

def getplate_num():
    file = open("Index.json", "r")
    data = json.load(file)
    file.close()
    return data["Plate_num"]    

def uploadCarStatus(status):
    carStatus = status

    doc_ref = db.collection("carInfo").document(getindex())

    #doc_path = "/test/X927gDJ5Q8b6bRGeudtv"

    # doc_ref提供一個set的方法，input必須是dictionary

    doc_ref.update({"carStatus": carStatus, "uploadTime":firestore.SERVER_TIMESTAMP})
    
def getStatus():
    doc_ref = db.collection("carInfo").document(getindex())
    #print(doc_ref.get().to_dict()["car_Status"])
    # doc_ref提供一個set的方法，input必須是dictionary
    return doc_ref.get().to_dict()["carStatus"]

def uploadBlowed(blowed):
    blow = blowed
    doc_ref = db.collection("carInfo").document(getindex())
    doc_ref.update({"Blowed": blowed, "uploadTime":firestore.SERVER_TIMESTAMP})

def getBlowed():
    doc_ref = db.collection("carInfo").document(getindex())
    return doc_ref.get().to_dict()["Blowed"]

def uploadPosition(lat,lon): #input is string
    latitude = float(lat)
    longitude = float(lon)
    doc_ref = db.collection("carInfo").document(getindex())
    doc_ref.update({"gpsLocation": GeoPoint(latitude, longitude), "uploadTime":firestore.SERVER_TIMESTAMP})

def getPosition():
    doc_ref = db.collection("carInfo").document(getindex())
    return doc_ref.get().to_dict()["gpsLocation"].latitude,doc_ref.get().to_dict()["gpsLocation"].longitude


def uploadHighSusTime():
    doc_ref = db.collection("carInfo").document(getindex())
    count = doc_ref.get().to_dict()["HighSusTime"]
    count += 1
    doc_ref.update({"HighSusTime": count, "uploadTime":firestore.SERVER_TIMESTAMP})

def uploadPlateNum():
     doc_ref = db.collection("carInfo").document(getindex())
     doc_ref.update({"licensePlateNum": getplate_num(), "uploadTime":firestore.SERVER_TIMESTAMP})


def uploadBlowingRecord(alvalue):
    alcohol_value = alvalue

    #db.collection("blowingRecord").doc("LA").set({
    #    name: "Los Angeles",
    #    state: "CA",
    #    country: "USA"
    #})
    
    db.collection('blowingRecord').add({
        "carId": getindex(),
        "time": firestore.SERVER_TIMESTAMP,
        "value": alcohol_value
      })
    
    

#uploadBlowingRecord(0.44)
