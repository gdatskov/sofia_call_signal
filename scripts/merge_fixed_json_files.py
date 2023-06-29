import json
import os

data_file_names = ['address.json',
                   'answers.json',
                   'comments.json',
                   'data.json',
                   'history.json',
                   'signal.json',
                   'status.json']

src_data_dir = '../available_data/manipulated_files'
dst_data_dir = '../available_data'
files_folders = os.listdir(src_data_dir)

# Start anew
for file in data_file_names:
    file_path = '/'.join([dst_data_dir, file])
    if os.path.exists(file_path):
        os.remove(file_path)

# Join all data files into the new files
for folder in files_folders:
    src_folder = '/'.join([src_data_dir, folder])
    files_in_folder = os.listdir(src_folder)
    for filename in files_in_folder:
        # if filename in data_file_names:
        #     with open('/'.join([src_folder, filename]), 'r', encoding='utf-8') as read_file:
        #         data = read_file.readlines()
        #         if not data[-1].endswith('}'):
        #             data = data[:-1]
        #     with open('/'.join([dst_data_dir, filename]), 'a', encoding='utf-8') as write_file:
        #         write_file.writelines(data)
        if filename in data_file_names:
            data = []
            with open(os.path.join(src_folder, filename), 'r', encoding='utf-8') as read_file:
                for line in read_file:
                    try:
                        line_data = json.loads(line)
                        data.append(line_data)
                    except json.decoder.JSONDecodeError as e:
                        print(f'Error: {e}')
                        print('File: ' f'{os.path.join(src_folder, filename)}')
                        print('Value: ' f'{line_data}')
                        print()
            with open(os.path.join(dst_data_dir, filename), 'a', encoding='utf-8') as write_file:
                for line_data in data:
                    json.dump(line_data, write_file, ensure_ascii=False)
                    write_file.write('\n')
