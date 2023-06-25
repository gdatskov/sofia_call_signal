import json


def fix_json_files(filepath):
    # Open and read badly formatted JSON file:
    with open(filepath, encoding='utf-8') as read_file:
        text = read_file.readlines()

    # Make new structures to write fixed data
    new_sample_text = []
    new_string = ''

    # Fix lines char by char, line by line:
    for line in text:
        new_string += line.strip()
        if line.endswith('}\n'):
            fix = new_string.replace('\n', '')
            new_sample_text.append(json.loads(fix))
            new_string = ''

    new_json_objects = '\n'.join(json.dumps(obj, ensure_ascii=False) for obj in new_sample_text)

    # Overwrite file with fixed JSON objects
    with open(filepath, 'w', encoding='utf-8') as write_file:
        write_file.write(new_json_objects)

