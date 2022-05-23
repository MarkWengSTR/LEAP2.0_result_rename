import glob
import json
import os
import zipfile

CURRENT_FILE = os.getcwd()
HIGHEST_FLOAT_POINT = '.3'

def unzip(data: dict) -> dict:
    with zipfile.ZipFile(data['zip_file'], 'r') as zip_file:
        zip_file.extractall('./' + data['unzip_folder_name'])

    data['res'] = True

    return data

def check_if_float_voltage(corrected_name: str) -> bool:
    words_with_kv = corrected_name.split()[-1].split('_')

    if len(words_with_kv) == 1:
        return False

    return True

def correct_float_voltage_name(unadd_float_name: str) -> str:
    name_words_list = unadd_float_name.split()

    name_words_list[-2] = name_words_list[-2] + HIGHEST_FLOAT_POINT

    name_words_list[-1] = 'kV.txt'

    return ' '.join(name_words_list)

def correct_file_name(file_name: str, measurement: str) -> str:
    corrected_name = ''

    try:
        if measurement == 'PD':
            corrected_name = measurement + file_name.split(measurement)[1]
        elif measurement == 'TD':
            corrected_name = file_name.split('Data ')[1]
    except:
        print("not avaliable measurement")

    if check_if_float_voltage(corrected_name):
        return correct_float_voltage_name(corrected_name)
    else:
        return corrected_name

def rename_file(file: str, measurement) -> str:
    corrected_path = os.path.join(data['unzip_folder_path'], correct_file_name(file, measurement))

    os.rename(
        os.path.join(data['unzip_folder_path'], file),
        corrected_path
    )

    return corrected_path


def rename_files(data: dict) -> dict:
    if data['res']:
        data['res'] = False

        all_files = os.listdir(data['unzip_folder_path'])

        for file in filter(lambda file: 'PD' in file, all_files):
            data['result'].append(rename_file(file, 'PD'))
        for file in filter(lambda file: 'TD' in file, all_files):
            data['result'].append(rename_file(file, 'TD'))

    data['res'] = True

    return data

if __name__ == "__main__":
    leap_zip_file = glob.glob(CURRENT_FILE + '\\*.zip')[0]
    unzip_folder_name = "rawdata"

    data = {
        "zip_file": leap_zip_file,
        "unzip_folder_name": unzip_folder_name,
        "unzip_folder_path": os.path.join(CURRENT_FILE, unzip_folder_name),
        "res": False,
        "result": []
    }

    data = unzip(data) and \
        rename_files(data)

    print(json.dumps(data, sort_keys=True, indent=4))
else:
    print("not able to unzip")
