import json

import numpy
import pandas

datafiledir = '../available_data/data.json'

with open(datafiledir, encoding='utf-8') as file:
    text = file.readlines()

sample = text[0:10]

# new_sample_text = []
# new_string = ''
# for x in text:
#     new_string += x.strip()
#     if x == '}\n':
#         fix = new_string.replace('\n', '')
#         new_sample_text.append(fix)
#         new_string = ''

# ChatGPT try 1
# new_sample_text = []
# new_string = ''
# for x in text:
#     new_string += x.strip()
#     if x == '}\n':
#         fix = new_string.replace('\n', '')
#         new_sample_text.append(json.loads(fix))
#         new_string = ''
#
# new_json_structure = json.dumps(new_sample_text, ensure_ascii=False)

# ChatGPT try 2
# new_sample_text = []
# new_string = ''
# for x in text:
#     new_string += x.strip()
#     if x == '}\n':
#         fix = new_string.replace('\n', '')
#         new_sample_text.append(json.loads(fix))
#         new_string = ''
#
# new_json_structure = '\n'.join(json.dumps(obj) for obj in new_sample_text)

# ChatGPT try 3
new_sample_text = []
new_string = ''
for x in text:
    new_string += x
    if x == '}\n':
        fix = new_string.replace('\n', '')
        new_sample_text.append(json.loads(fix))
        new_string = ''

new_json_structure = '\n'.join(json.dumps(obj, ensure_ascii=False) for obj in new_sample_text)


with open(datafiledir, 'w', encoding='utf-8') as file:
    file.write(new_json_structure)

with open('../../signals/spiders/scraped_data/2023-06-23_21-06-30/address.json', 'r', encoding='utf-8') as file:
    actual_json = file.readlines()
actual_json_dumps = json.dumps(actual_json, ensure_ascii=False)

with open(datafiledir, 'r', encoding='utf-8') as file:
    new_json_file = file.readlines()
new_json_file_dumps = json.dumps(new_json_file, ensure_ascii=False)

new_json_file_dataframe_test = pandas.read_json(new_json_file_dumps, lines=True)
print('new_json_file_dataframe_test')
print(numpy.array(new_json_file_dataframe_test)[0])

new_json_structure_dataframe_test = pandas.read_json(new_json_structure, lines=True)
print('new_json_structure_dataframe_test')
print(numpy.array(new_json_structure_dataframe_test)[0])

actual_json_file_dataframe = pandas.read_json('../../signals/spiders/scraped_data/2023-06-23_21-06-30/address.json', lines=True)
print('actual_json_file_dataframe')
print(numpy.array(actual_json_file_dataframe)[0])

actual_json_structure_dataframe = pandas.read_json(actual_json_dumps, lines=True)
print('actual_json_dumps_dataframe')
print(numpy.array(actual_json_file_dataframe)[0])

# def fix_json_padding(list_to_fix):
#     new_list = []
#     new_string = ''
#     for x in new_list:
#         new_string += x.strip()
#         if x == '}\n':
#             fix = new_string.replace('\n', '')
#             new_sample_text.append(new_string)
#             new_string = ''
