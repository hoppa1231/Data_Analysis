SIZE_WINDOW = (1024, 576)               # Размер окна приложения

SIZE_TOOLS_ICON = (24, 24)              # Размер иконок инструментов

SIZE_TOOLS_BUTTON = 30                  # Сторона кнопки инструментов

SIZE_LEGEND = 250                  # Сторона кнопки инструментов

SPACE = 10                              # Ширина стандартного интервала

FEEDBACK_WEIGHT = 250                   # Ширина отладочного лейбла

INFO_WEIGHT = 250                       # Ширина информационного лейбла

SIZE_DIALOG_CHOOSE = (400, 500)         # Размер диалогового окна Выбор SPN

PATH_FILE_SPN = "data/SPN_parts.txt"    # Путь до SPN выжимки

PATH_FILE_PGN = "data/PGN_parts.txt"    # Путь до PGN выжимки

EXTEND_ERRORBAR = None                  # Отрисовка доверительной вероятности

DPI_SAVE = 300                          # Качество сохраненного графика

FILE_SPN = ''.join(open(PATH_FILE_SPN).readlines())
FILE_PGN = ''.join(open(PATH_FILE_PGN).readlines())