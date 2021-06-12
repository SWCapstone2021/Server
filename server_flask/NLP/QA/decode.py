import json

# with open('models/predictions_.json', 'r') as json_file:
#     prediction = json.load(json_file)
#
# print(prediction)
#
# with open('prediction.json', 'w', encoding='utf-8') as outfile:
#     json.dump(prediction, outfile, ensure_ascii=False, indent=4)
#

with open('data/KorQuAD_DEV.json', 'r') as json_file:
    prediction = json.load(json_file)

with open('data/KorQuAD_DEV.json', 'w', encoding='utf-8') as outfile:
    json.dump(prediction, outfile, ensure_ascii=False, indent=4)
