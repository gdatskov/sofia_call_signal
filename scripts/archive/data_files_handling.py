import os

from signals.scripts.archive.fix_json_files_function import fix_json_files

data_file_names = ['address.json',
                   'answers.json',
                   'comments.json',
                   'data.json',
                   'history.json',
                   'signal.json',
                   'status.json']

data_dir = '../../signals/spiders/scraped_data/'

folders_in_data_dir = os.listdir(data_dir)

datafiledir = '../available_data'

# Try to make desired directory
try:
    os.mkdir(datafiledir)
except FileExistsError:
    print("Directory already exists.")
    print("Continuing...")


# Create or truncate the files
full_data_filepath = []
for filename in data_file_names:
    filepath = "/".join([datafiledir, filename])
    file = open(filepath, 'w')
    file.close()
    full_data_filepath.append(filepath)
print(full_data_filepath)

# Join all data files into the new files
for folder in folders_in_data_dir:
    if folder.startswith('2023'):
        data_folder_path = os.path.join(data_dir, folder)
        files_in_folder = os.listdir(data_folder_path)
        for filename in files_in_folder:
            if filename in data_file_names:
                with open(os.path.join(data_folder_path, filename), 'r', encoding='utf-8') as read_file:
                    data = read_file.readlines()
                with open(os.path.join(datafiledir, filename), 'a', encoding='utf-8') as write_file:
                    write_file.writelines(data)

full_data_filepath = [
    '../available_data/address.json',
    '../available_data/answers.json',
    '../available_data/comments.json',
    '../available_data/data.json',
    '../available_data/history.json',
    '../available_data/signal.json',
    '../available_data/status.json'
]

for file in full_data_filepath:
    fix_json_files(file)

