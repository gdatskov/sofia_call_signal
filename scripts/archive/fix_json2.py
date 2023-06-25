import json


def fix_json_files2(filepath):
    # Open and read the badly formatted JSON file
    with open(filepath, encoding='utf-8') as read_file:
        text = read_file.read()

    # Remove whitespaces and newlines
    text = text.replace(" ", "").replace("\n", "")

    # Replace '}{' with '}\n{'
    fixed_text = text.replace("}{", "}\n{")

    # Write the fixed JSON text back to the file
    with open(filepath, 'w', encoding='utf-8') as write_file:
        write_file.write(fixed_text)