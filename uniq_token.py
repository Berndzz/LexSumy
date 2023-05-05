# import pandas as pd

# read_json = pd.read_json('util\label_mini_2.json')

# def text_to_string(row):
#   text = row['label']
#   text = ','.join(' '.join(j['text'].title().split())for j in text) # .title() , .capitalize()
#   return text

# read_json['lbl'] = read_json.apply(text_to_string,axis=1)
# read_json['lsl'] = read_json['lbl'].str.split(",")
# temp = read_json['lsl'].tolist()
# unique_token = []
# for doc in temp:
#   for sentence in doc:
#     unique_token.append(sentence)

# unique_token.append('Ajat Temuai Datai')
# unique_token.append('Dayak Mualang')
# unique_token.append('Dayak Iban')
# unique_token.append('Ki Naryo')
# unique_token.append('Tari Belian bawo')
# unique_token.append('Tari sajojo')
import pandas as pd
import json

try:
    with open('util/label_mini_2.json') as f:
        data = json.load(f)
        read_json = pd.json_normalize(data)
except Exception as e:
    print(f"Error reading JSON file: {e}")
    read_json = pd.DataFrame()


def text_to_string(row):
    text = row['label']
    text = ','.join(' '.join(j['text'].title().split())
                    for j in text)  # .title() , .capitalize()
    return text


if not read_json.empty:
    read_json['lbl'] = read_json.apply(text_to_string, axis=1)
    read_json['lsl'] = read_json['lbl'].str.split(",")
    temp = read_json['lsl'].tolist()
    unique_token = []
    for doc in temp:
        for sentence in doc:
            unique_token.append(sentence)

    unique_token.append('Ajat Temuai Datai')
    unique_token.append('Dayak Mualang')
    unique_token.append('Dayak Iban')
    unique_token.append('Ki Naryo')
    unique_token.append('Tari Belian bawo')
    unique_token.append('Tari sajojo')
else:
    unique_token = []
