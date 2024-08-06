import pymupdf
import pandas
import re
import pathlib
import os
import time
from tkinter import filedialog as fd


FILETYPES = (('pdf files', '*.pdf'), ('all files', '*.*'))
NAME_OF_CSV = ''


class PDFHandler:

    @staticmethod
    def open_file(name_of_new_file):
        pdf_file_path = fd.askopenfile(filetypes=FILETYPES, initialdir="~/")

        with pymupdf.open(pdf_file_path) as doc:
            text = chr(12).join([page.get_text() for page in doc])
            pathlib.Path(f"{name_of_new_file}" + ".txt").write_bytes(text.encode())
            while not pathlib.Path(name_of_new_file):
                try:
                    file_size = os.path.getsize(f"{name_of_new_file}")
                    file_path = pathlib.Path(f"{name_of_new_file}")
                finally:
                    return file_size, file_path
            else:
                time.sleep(1)
                pass

    @staticmethod
    # noinspection RegExpSimplifiable
    def get_pdf_data(text_from_pdf, name_of_new_file):
        """
        This function parses through the data to compare the part numbers in the newly formed txt file.
        For extron parts, the part numbers come in two formats: 00-0000-00 or 00-000-00. If these part
        numbers are found the re.findall method saves those part numbers in a list.
        :return:
        """
        with open(f"{text_from_pdf}", "r", encoding="UTF-8") as new_data:
            text_in_data = str(new_data.readlines())
            part_nums = re.findall("[0-9][0-9][-][0-9][0-9][0-9][0-9][-][0-9][0-9]", text_in_data)
            extra_part_nums = re.findall("[0-9][0-9[-][0-9][0-9][0-9][-][0-9][0-9]", text_in_data)
        # This block parses through the data and writes the part numbers to a new file for later analysis.
        with open(f"{name_of_new_file}", "a", encoding="UTF=8") as new_file:

            for part in part_nums:
                new_file.write(f"{part},\n")
            for extra in extra_part_nums:
                new_file.write(f"{extra},\n")

    @staticmethod
    def get_objects(csv_file, ):
        """
        This method utilizes the pandas library to read the product_data.csv and iterates through the rows.
        It then adds each part number that was written to the file from the get_pdf_data method in extract_pdf.py.
        The final function returns the list of part numbers to be used in the WireMapWindow class in gui.py.
        :return:
        """
        app_data = pandas.read_csv(f'{csv_file}', index_col=0)
        new_list = []

        with open(f'{args}', 'r') as doc:
            user_data = doc.readlines()

            for index, row in app_data.iterrows():
                for i in range(len(user_data)):
                    if user_data[i].strip() in row['part_num'] or user_data[i].strip() in row['model']:
                        new_list.append(f"{row['model']}: {user_data[i].strip()} | {row['description']}")

        trimmed_list = []
        num_input = 0
        num_output = 0
        num_mics = 0
        num_matrix = 0

        for i in range(len(new_list)):
            match1 = re.findall("Output Board", new_list[i])
            match2 = re.findall("Input Board", new_list[i])
            match3 = re.findall("Microphone", new_list[i])
            match4 = re.findall("Audio Matrix", new_list[i])

            if match1:
                num_output += 1
                trimmed_list.append(f"{match1[i % len(match1)]}-{num_output}")
            elif match2:
                num_input += 1
                trimmed_list.append(f"{match2[i % len(match2)]}-{num_input}")
            elif match3:
                num_mics += 1
                trimmed_list.append(f"{match3[i % len(match3)]}-{num_mics}")
            elif match4:
                num_matrix += 1
                trimmed_list.append(f"{match4[i % len(match4)]}-{num_matrix}")
            else:
                continue

        return trimmed_list

    @staticmethod
    def get_wiremap_objects():
        # Call the get_objects function and store it inside a variable.
        list_apps = PDFHandler.get_objects(csv_file='')
        # Creates a blank list to store the finalized part numbers and the corresponding description
        # and model names.
        final_list = []
        for pos in range(len(list_apps)):
            final_list.append(f"{list_apps[pos]}")

        return final_list


f_name = input("Please provide a name for the new file: ")
PDFHandler.open_file(f"{f_name}")
