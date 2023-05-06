import pandas as pd

try:
    read_json = pd.read_json(r'util/label_mini_2.json')
except FileNotFoundError:
    print("File not found.")
    # handle the exception as needed


def text_to_string(row):
    text = row['label']
    text = ','.join(' '.join(j['text'].title().split())
                    for j in text)  # .title() , .capitalize()
    return text


read_json['lbl'] = read_json.apply(text_to_string, axis=1)
read_json['lsl'] = read_json['lbl'].str.split(",")
temp = read_json['lsl'].tolist()

unique_token = [sentence for doc in temp for sentence in doc]
unique_token.extend(['Ajat Temuai Datai', 'Dayak Mualang',
                    'Dayak Iban', 'Ki Naryo', 'Tari Belian bawo', 'Tari sajojo'])
