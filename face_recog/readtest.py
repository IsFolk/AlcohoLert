import json


file = open("Index.json", "r")

data = json.load(file)

print(data["Index"])