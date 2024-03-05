# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def getStatus():
    doc_ref = db.collection("carInfo").document("001")

    # doc_ref提供一個set的方法，input必須是dictionary
    return doc_ref.get().to_dict()["car_Status"]
