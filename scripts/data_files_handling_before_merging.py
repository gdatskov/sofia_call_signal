import os
import shutil

from signals.scripts.fix_json_before_merging import fix_json_files

data_file_names = ['address.json',
                   'answers.json',
                   'comments.json',
                   'data.json',
                   'history.json',
                   'signal.json',
                   'status.json']

src_data_dir = '../signals/spiders/scraped_data'

folders_in_data_dir = os.listdir(src_data_dir)

dst_data_dir = '../available_data/manipulated_files'

# Try to make desired directories
try:
    os.mkdir(dst_data_dir)
except FileExistsError:
    pass

# Copy files for further manipulation
for folder in folders_in_data_dir:
    if folder.startswith('2023'):
        try:
            os.mkdir(os.path.join(dst_data_dir, folder))
        except FileExistsError:
            pass
        src_data_sub_dir = '/'.join([src_data_dir, folder])
        dst_data_sub_dir = '/'.join([dst_data_dir, folder])
        src_file_names = os.listdir('/'.join([src_data_dir, folder]))
        for filename in src_file_names:
            if filename.endswith('.json'):
                src = '/'.join([src_data_sub_dir, filename])
                dst = '/'.join([dst_data_sub_dir, filename])
                shutil.copy(src, dst)

new_files_folders = os.listdir(dst_data_dir)
for folder in new_files_folders:
    sub_dir = '/'.join([dst_data_dir, folder])
    sub_folders = os.listdir(sub_dir)
    for sub in sub_folders:
        file_path = '/'.join([sub_dir, sub])
        print(file_path)
        fix_json_files(file_path)

