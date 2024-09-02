import pandas as pd
import numpy as np

from settings import *

SPN_Select = {}
# SPN_Select[SPN] = 1/0
SPN_PGN = {}
# SPN_PGN[SPN] = PGN
SPN_Position = {}
# SPN_Position[SPN] = Position Bits/Bytes (str)
SPN_Unit = {}
# SPN_Unit[SPN] = Unit of measurement (str)
SPN_Resolution = {}
# SPN_Resolution[SPN] = Resolution value (float)
SPN_Offset = {}
# SPN_Offset[SPN] = Offset value (float)
SPN_Info = {}
# SPN_Info[SPN] = Full Information (str)
SPN_Range = {}
# SPN_Range[SPN] = Value to Value (tuple)
SPN_Name = {}


def get_pgn_unique(data):
    """ Функция получения всех уникальных PGN в INTEGER """
    try:
        return [i for i in data.iloc[:, -1].unique()]
    except:
        print("ERROR: get_pgn_unique()")
        return []


def find_pgn_info(pgn):
    """ Функция получения информации о PGN из документации """
    text = FILE_PGN
    res = text.find(f"pgn{pgn}")
    if res != -1:
        text = text[res:]
        info = text[:text.find("\n\n")]
        first_line = text[:text.find('\n')]
        name = first_line[first_line.find('-') + 1:first_line.rfind('-')].strip()
        list_spn = pars_spn(info, pgn)
    else:
        return 0

    return [name, info, list_spn]


def pars_spn(text : str, pgn : int):
    """ Функция парсит все SPN и позицию бит/байт из информации о PGN """
    text = text[text.find("Description SPN"):]
    spn_result = []
    for line in text.split('\n')[1:]:
        if line[0].isdigit():
            position_value = line[:line.find(" b")]
            spn = int(line.split()[-1])

            fl_write = False
            name_spn = ''
            for symbol in line:
                if symbol.isupper():
                    fl_write = True
                if symbol == '\n':
                    break
                if fl_write:
                    name_spn += symbol

            SPN_Select[spn] = 0
            SPN_PGN[spn] = pgn
            SPN_Position[spn] = position_value
            SPN_Name[spn] = name_spn

            get_URO(spn)

            spn_result.append((spn, name_spn))
        else:
            break
    return spn_result


def get_URO(spn):
    """ Функция для заполнения словарей:
            Разрешение, Информация, Сдвиг, Диапазон, Ед. Измерения """
    SPN_Info[spn], info = None, None
    SPN_Resolution[spn], resolution = None, None
    SPN_Unit[spn], unit = None, None
    SPN_Offset[spn], offset_value = None, None
    SPN_Range[spn], range_value = None, None

    text = FILE_SPN
    res = text.find(f"spn{spn}")
    if res != -1:
        text = text[res:]
        info = text[:text.find("\n\n")]

        for line in info.split('\n'):
            if "Resolution:" in line:
                resolution = line.split()[1].replace('/bit', '')
                try:
                    resolution = eval(resolution) if '/' in resolution else float(resolution)
                except:
                    print(f"ERROR: {line}")
                    resolution = None
                offset_value = line.split(' , ')[-1]
                if "offset" in line:
                    try:
                        offset_value = float(offset_value.split()[0])
                    except ValueError:
                        s = ''.join([i for i in offset_value.split()[0] if i.isdigit() or i == '-'])
                        offset_value = float(s)

            if "Data Range:" in line:
                line_range = list(line.replace(',', '').split())
                range_value = []
                x = 0
                for i, part in enumerate(line_range):
                    try:
                        range_value.append(float(part))
                        x = i
                    except:
                        continue
                unit = ' '.join(line_range[x+1:])



        SPN_Info[spn] = info
        SPN_Resolution[spn] = resolution
        SPN_Unit[spn] = unit
        SPN_Offset[spn] = offset_value
        SPN_Range[spn] = range_value



def descript_position(string : str):
    """ Функция расшифровки позиции бит/байт в данных """
    array = list(string.split('-'))
    length = len(array)
    type_pos = ""
    res = []
    # 1 element => 1.2 2 or 1 2
    # 2 element => 1-2 2 or 1.2-2 14
    if length == 1:
        array = list(array[0].split('.'))

        # example: 1.2 2
        if len(array) == 2:
            res = [int(array[0])] + list(map(int, array[1].split()))
            type_pos = 'D'

        # example: 1 2
        else:
            res = list(map(int, array[0].split()))
            type_pos = "N"

    if length == 2:
        temp_array = list(array[0].split('.'))

        # example: 1-2 2
        if len(temp_array) == 1:
            res = list(map(int, array[1].split()))
            res[0] = int(array[0])
            type_pos = "B"

        # example: 1.2-2 14
        else:
            res = list(map(int, temp_array)) + list(map(int, array[1].split()))
            type_pos = "A"

    return type_pos, res


def filter_data_pgn(data, pgn):
    return data.loc[data["PGN"] == pgn]


def load_file(file_name):
    """ Открытие файла как CSV """

    def extract_pgn(packet_id):
        return int(packet_id[2:6], 16)
    try:
        if ".csv" not in file_name:
            raise TypeError
        data = pd.read_csv(file_name, sep=";")
        data["PGN"] = data.iloc[:, 0].apply(extract_pgn)
    except:
        print("ERROR: process_file()")
        return 0
    return data


def extract_value(filter_data, type_pos : str, array_pos : list):
    """ Достаем необходимые значения из данных для построения графиков
        array_pos задает маску, по которой извлекаем необходимое """
    datetime = filter_data.iloc[:, -2].apply(lambda x: x[:x.find('.')]).rename("DateTime")

    def hex_to_bin(x):
        res = bin(int(x, 16))[2:]
        length = len(res)
        res = (8-length)*"0" + res
        return res

    def HEX_split(x):
        bin_x = hex_to_bin(x)
        return bin_x[array_pos[1]-1:array_pos[1] + array_pos[-1]-1]

    if type_pos == "D":
        integer = filter_data.iloc[:, array_pos[0]].apply(HEX_split)
        integer = integer.apply(lambda x: int(x, 2)).rename("Value").to_frame()

    elif type_pos == "A":
        integer = filter_data.iloc[:, list(range(array_pos[0] + array_pos[1]-1, array_pos[0]-1, -1))] \
            .apply(lambda x: HEX_split(''.join(x)))
        integer = integer.apply(lambda x: int(''.join(x), 2), axis=1).rename("Value").to_frame()

    else:
        integer = filter_data.iloc[:, list(range(array_pos[0] + array_pos[1]-1, array_pos[0]-1, -1))] \
            .apply(lambda x: ''.join(map(hex_to_bin, x)), axis=1)
        integer = integer.apply(lambda x: int(x, 2)).rename("Value").to_frame()

    result_data = pd.concat([datetime, integer], axis=1)

    return result_data


def find_y_lim(data, i, count):
    mx = data["Value"].max()
    mn = data["Value"].min()
    step = mx - mn

    if round(step) == 0:
        step = 1

    y_max = (count - i - 1) * step + mx
    y_min = mn - i * step

    return y_max, y_min

