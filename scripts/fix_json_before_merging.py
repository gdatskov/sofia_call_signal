def fix_json_files(filepath):
    # Open and read the badly formatted JSON file
    with open(filepath, encoding='utf-8') as read_file:
        text = read_file.read()

    # Remove leading and trailing spaces from each line
    stripped_lines = [line.strip() for line in text.split('\n')]

    # Join the stripped lines
    stripped_text = ''.join(stripped_lines)

    # Replace '}{' with '}\n{'
    fixed_text = stripped_text.replace("}{", "}\n{")

    # Write the fixed JSON text back to the file
    with open(filepath, 'w', encoding='utf-8') as write_file:
        write_file.write(fixed_text)
