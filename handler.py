import pandas as pd
import pathlib
import pymupdf
import re
import os
import time


FILETYPES = (('pdf files', '*.pdf'), ('all files', '*.*'))


class DataExtract:

    def __init__(self):
        pass

    def convert_csv(self, **kwargs):
        csv_file = kwargs['path_to_file']
        app_data = pd.read_csv(f'{csv_file}', index_col=0)
        return app_data

    def convert_pdf(self, **kwargs):
        path_to_pdf = kwargs['path_to_pdf']
        new_file = kwargs['new_file_name']
        with pymupdf.open(path_to_pdf) as doc:
            text = chr(12).join([page.get_text() for page in doc])
            pathlib.Path(f"{new_file}" + ".txt").write_bytes(text.encode())
            while not pathlib.Path(new_file):
                try:
                    file_size = os.path.getsize(f"{new_file}")
                    file_path = pathlib.Path(f"{new_file}")
                finally:
                    return file_size, file_path
            else:
                time.sleep(1)
                pass

    def extract_pdf_data(self, **kwargs):
        path_to_file = kwargs['file_path']
        pattern_1 = kwargs['pattern1']
        pattern_2 = kwargs['pattern2']
        new_file = kwargs['name_of_new_file']

        with open(f"{path_to_file}", "r", encoding="UTF-8") as new_data:
            text_in_data = str(new_data.readlines())
            part_nums = re.findall(f"{pattern_1}", text_in_data)
            extra_part_nums = re.findall(f"{pattern_2}", text_in_data)
        # This block parses through the data and writes the part numbers to a new file for later analysis.
        with open(f"{new_file}", "a", encoding="UTF=8") as new_file:

            for part in part_nums:
                new_file.write(f"{part},\n")
            for extra in extra_part_nums:
                new_file.write(f"{extra},\n")

    def generate_objects(self, **kwargs):
        path_to_file = kwargs['file_path']
        app_data = kwargs['csv_data']
        new_list = []
        with open(f'{path_to_file}', 'r') as doc:
            user_data = doc.readlines()

            for index, row in app_data.iterrows():
                for i in range(len(user_data)):
                    if user_data[i].strip() in row['part_num'] or user_data[i].strip() in row['model']:
                        new_list.append(f"{row['model']}: {user_data[i].strip()} | {row['description']}")

        return new_list
