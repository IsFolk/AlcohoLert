# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('./serviceAccount.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()


doc_ref = db.collection("carInfo").document("001")

#doc_path = "/test/X927gDJ5Q8b6bRGeudtv"

# doc_ref提供一個set的方法，input必須是dictionary
#doc_ref.update({"car_Status": 1})
print(doc_ref.get().to_dict()["car_Status"])