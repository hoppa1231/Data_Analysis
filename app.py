# -*- coding: utf-8 -*-
#
# Требования к файлу Лога:
#   1. Расширение .CSV
#   2. Порядок столбцов: ID, Data (8 столбцов), DateTime
#

import sys

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QAction, QIcon, QPixmap, QColor)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QPushButton, QStatusBar, QWidget, QFileDialog, QLabel, QDialog, QHBoxLayout, QVBoxLayout,
    QScrollArea, QListWidget, QListWidgetItem)

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

from toolbarQT import NavigationToolbar

from settings import *
from extend import *
from translater import translate_to_russian


class UiMainWindow(object):
    def setup(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(*SIZE_WINDOW)
        MainWindow.setWindowIcon(QIcon(PATH_ICON + 'icon_ptz_graph.ico'))

        ''' Меню -> Файл -> Открыть файл '''
        self.actionOpen_File = QAction(MainWindow)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.actionOpen_File.triggered.connect(self.open_file)

        ''' Меню -> Файл -> Сохранить '''
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionExport.triggered.connect(self.save_plot)

        ''' Меню -> Помощь -> Информация '''
        self.actionInfo = QAction(MainWindow)
        self.actionInfo.setObjectName(u"actionInfo")

        ''' Меню -> Настройки '''
        self.actionsettings = QAction(MainWindow)
        self.actionsettings.setObjectName(u"actionsettings")

        ''' Меню -> Настройки -> Параметры '''
        self.actionProperties = QAction(MainWindow)
        self.actionProperties.setObjectName(u"actionProperties")

        ''' Меню -> Настройки -> Стиль -> Обычный '''
        self.actionDefault = QAction(MainWindow)
        self.actionDefault.setObjectName(u"actionDefault")

        ''' Меню -> Настройки -> Стиль -> Темный '''
        self.actionDark = QAction(MainWindow)
        self.actionDark.setObjectName(u"actionDark")

        ''' Главный виджет - Полотно '''
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.central_layout = QVBoxLayout()
        self.centralwidget.setLayout(self.central_layout)


        '''  Панель инструментов '''
        self.widget_tools = QWidget()
        self.widget_tools.setObjectName(u"widget_tools")
        self.widget_tools.setFixedHeight(SIZE_TOOLS_BUTTON+1)
        self.widget_tools.setStyleSheet(u"border-bottom: 1px solid #D0D0D0;")
        self.widget_tools_layout = QHBoxLayout()
        self.widget_tools_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_tools_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.widget_tools.setLayout(self.widget_tools_layout)
        self.central_layout.addWidget(self.widget_tools)

        ''' Инструменты -> Открыть файл '''
        self.openFile_tools = QPushButton()
        self.openFile_tools.setObjectName(u"openFile_tools")
        self.openFile_tools.setFixedSize(SIZE_TOOLS_BUTTON+1, SIZE_TOOLS_BUTTON+1)
        icon = QIcon(PATH_ICON + "open_file.png")
        self.openFile_tools.setIcon(icon)
        self.openFile_tools.setFlat(True)
        self.openFile_tools.setIconSize(QSize(*SIZE_TOOLS_ICON))
        self.openFile_tools.clicked.connect(self.open_file)
        self.openFile_tools.setToolTip("Открыть файл")

        ''' Инструменты -> Сохранить '''
        self.save_tools = QPushButton()
        self.save_tools.setObjectName(u"save_tools")
        self.save_tools.setFixedSize(SIZE_TOOLS_BUTTON+1, SIZE_TOOLS_BUTTON+1)
        icon1 = QIcon(PATH_ICON + "save_file.png")
        self.save_tools.setIcon(icon1)
        self.save_tools.setFlat(True)
        self.save_tools.setIconSize(QSize(*SIZE_TOOLS_ICON))
        self.save_tools.clicked.connect(self.save_plot)
        self.save_tools.setToolTip("Сохранить график")

        ''' Инструменты -> Обновить '''
        self.drawGraph_tools = QPushButton()
        self.drawGraph_tools.setObjectName(u"movePlot_tools")
        self.drawGraph_tools.setFixedSize(SIZE_TOOLS_BUTTON+1, SIZE_TOOLS_BUTTON+1)
        icon4 = QIcon(PATH_ICON + "repeat_draw.png")
        self.drawGraph_tools.setIcon(icon4)
        self.drawGraph_tools.setFlat(True)
        self.drawGraph_tools.setIconSize(QSize(*SIZE_TOOLS_ICON))
        self.drawGraph_tools.clicked.connect(self.choose_pgn)
        self.drawGraph_tools.setToolTip("Построить еще раз")

        self.widget_tools_layout.addWidget(self.openFile_tools, alignment=Qt.AlignmentFlag.AlignBaseline)
        self.widget_tools_layout.addWidget(self.save_tools, alignment=Qt.AlignmentFlag.AlignBaseline)
        self.widget_tools_layout.addWidget(self.drawGraph_tools, alignment=Qt.AlignmentFlag.AlignLeft)

        ''' Рабочая область '''
        self.workArea = QWidget()
        self.workArea.setObjectName(u"workArea")
        self.workArea_layout = QHBoxLayout()
        self.workArea.setLayout(self.workArea_layout)
        self.central_layout.addWidget(self.workArea)


        ''' Виджет для графиков '''
        self.areaPlot = QWidget()
        self.areaPlot.setObjectName(u"areaPlot")
        self.areaPlot.setGeometry(QRect(0, SIZE_TOOLS_BUTTON, SIZE_WINDOW[0]-SIZE_LEGEND, 501))
        self.areaPlot_layout = QVBoxLayout()
        self.areaPlot.setLayout(self.areaPlot_layout)
        self.workArea_layout.addWidget(self.areaPlot)


        ''' Зона для легенды '''
        self.legendWidget = QWidget()
        self.legendWidget.setObjectName(u"legendWidget")
        self.legendWidget.setGeometry(QRect(0, SIZE_TOOLS_BUTTON, SIZE_LEGEND, 501))
        self.legendWidget.setMinimumWidth(SIZE_LEGEND)
        self.legendWidget_layout = QVBoxLayout()
        self.legendWidget.setLayout(self.legendWidget_layout)
        self.workArea_layout.addWidget(self.legendWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        ''' Дерево Меню '''
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setFixedHeight(22)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuHelp.setGeometry(QRect(301, 125, 134, 72))
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuStyle = QMenu(self.menuSettings)
        self.menuStyle.setObjectName(u"menuStyle")
        MainWindow.setMenuBar(self.menubar)

        ''' Виджет для статусов '''
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"border-top: 1px solid #D0D0D0;")
        MainWindow.setStatusBar(self.statusbar)

        ''' Статус отладки '''
        self.feedback_label = QLabel(self.statusbar)
        self.feedback_label.setObjectName(u"feedbackLabel")
        self.feedback_label.setGeometry(QRect(SPACE, 0, FEEDBACK_WEIGHT, 20))

        ''' Статус информации '''
        self.info_label = QLabel(self.statusbar)
        self.info_label.setObjectName(u"infoLabel")
        self.info_label.setGeometry(QRect(SPACE*2+FEEDBACK_WEIGHT, 0, INFO_WEIGHT, 20))

        ''' Добавление кнопок в Меню '''
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuHelp.addAction(self.actionInfo)
        self.menuSettings.addAction(self.menuStyle.menuAction())
        self.menuSettings.addAction(self.actionProperties)
        self.menuStyle.addAction(self.actionDefault)
        self.menuStyle.addAction(self.actionDark)

        self.translate(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def translate(self, window):
        """ Обзываем элементы приложения """
        window.setWindowTitle(QCoreApplication.translate("MainWindow", u"Графический Анализатор", None))
        self.actionOpen_File.setText(QCoreApplication.translate("MainWindow", u"Открыть файл", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Сохранить", None))
        self.actionInfo.setText(QCoreApplication.translate("MainWindow", u"Информация", None))
        self.actionsettings.setText(QCoreApplication.translate("MainWindow", u"Настройки", None))
        self.actionProperties.setText(QCoreApplication.translate("MainWindow", u"Параметры", None))
        self.actionDefault.setText(QCoreApplication.translate("MainWindow", u"Обычный", None))
        self.actionDark.setText(QCoreApplication.translate("MainWindow", u"Темный", None))
        self.feedback_label.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Файл", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Помощь", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Настройки", None))
        self.menuStyle.setTitle(QCoreApplication.translate("MainWindow", u"Стиль", None))

    def open_file(self):
        """ Загрузка файла и открытие как CSV """
        file_name, _ = QFileDialog.getOpenFileName(MainWindow, "Открыть файл", "", "Все файлы (*)")
        if file_name:
            self.feedback_label.setText("Открывается...")
            ''' Загрузка файла '''
            self.data = load_file(file_name)
            if type(self.data) != int:
                self.feedback_label.setText("Успешно открыт")
            else:
                self.feedback_label.setText("Не удалось открыть файл")
            ''' Обработка файла '''
            self.process_file(self.data)

    def process_file(self, data):
        """ Функция вызывается после открытия файла распознает PGN и SPN """
        pgn_unique = get_pgn_unique(data)
        count_pgn = len(pgn_unique)
        count_detected_pgn = 0
        self.pgn_info = {}
        for pgn in pgn_unique:
            info = find_pgn_info(pgn)
            if info:
                self.pgn_info[pgn] = info
                count_detected_pgn += 1
            else:
                if 65280 <= pgn <= 65535:
                    print('+', pgn)
                else:
                    print(pgn)
        self.info_label.setText(f"Опознано {count_detected_pgn} из {count_pgn} PGN")

        self.choose_pgn()
        # self.pgn_info : Structure
        # [PGN (int)] = <Full Information> (list)

        # [PGN (int)][0] = Title PGN (str)
        # [PGN (int)][1] = Description PGN (str)
        # [PGN (int)][2] = <List SPN Information> (list)

        # [PGN (int)][2][0] = SPN (int)
        # [PGN (int)][2][1] = Title SPN (str)

    def choose_pgn(self):
        """ Функция вызова диалогового окна для выбора SPN """
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Выберите PGN")
        self.dialog.setModal(True)
        self.dialog.setFixedSize(SIZE_DIALOG_CHOOSE[0]+SPACE*2, SIZE_DIALOG_CHOOSE[1])

        ''' Scroll зона для списка PGN'''
        scroll_area_PGN = QScrollArea(self.dialog)
        scroll_area_PGN.setWidgetResizable(True)

        content_widget_PGN = QWidget()
        content_widget_PGN.setLayout(QVBoxLayout())
        self.list_pgn = QListWidget()

        ''' Добавляем все обнаруженные PGN '''
        for pgn, info in self.pgn_info.items():
            checkbox = QListWidgetItem(f"{pgn} {info[0]}")
            self.list_pgn.addItem(checkbox)
        self.list_pgn.itemSelectionChanged.connect(self.update_spn)

        content_widget_PGN.layout().addWidget(self.list_pgn)
        scroll_area_PGN.setWidget(content_widget_PGN)

        ''' Scroll зона для списка SPN'''
        scroll_area_SPN = QScrollArea(self.dialog)
        scroll_area_SPN.setWidgetResizable(True)

        content_widget_SPN = QWidget()
        content_widget_SPN.setLayout(QVBoxLayout())
        self.list_spn = QListWidget()

        content_widget_SPN.layout().addWidget(self.list_spn)
        scroll_area_SPN.setWidget(content_widget_SPN)
        self.list_spn.itemChanged.connect(self.checkbox_changed)

        ''' Добавление кнопки 'Выбрать' '''
        button = QPushButton("Выбрать")
        button.clicked.connect(self.accept_and_print)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area_PGN)
        layout.addSpacing(SPACE)
        layout.addWidget(scroll_area_SPN)
        layout.addWidget(button)
        self.dialog.setLayout(layout)

        self.dialog.exec()

    def update_spn(self):
        """ Вызывается, когда выбран PGN """

        self.list_spn.clear()
        selected_pgn = self.list_pgn.currentItem().text()
        pgn = int(selected_pgn[:selected_pgn.find(' ')])

        ''' 
        Выводим список SPN для выбранного PGN.
        В соответствии с SPN_Selected.
        '''
        for line_list_spn in self.pgn_info[pgn][2]:
            checkbox = QListWidgetItem(line_list_spn[1])
            checkbox.setFlags(checkbox.flags() | Qt.ItemFlag.ItemIsUserCheckable)

            ''' Отмечаем уже нажатые CheckBoxes '''
            if SPN_Select[line_list_spn[0]]: checkbox.setCheckState(Qt.CheckState.Checked)
            else: checkbox.setCheckState(Qt.CheckState.Unchecked)

            self.list_spn.addItem(checkbox)

    def checkbox_changed(self, item):
        """ Вызывается, когда изменяется состояние list_spn.
            Меняет состояние SPN_Selected на 1 или 0 """
        name_spn = item.text()
        spn = int(name_spn[name_spn.rfind(' '):])
        ''' Если включен, то так и записываем, если нет, то нет '''
        if item.checkState() == Qt.CheckState.Checked:
            SPN_Select[spn] = 1
        elif item.checkState() == Qt.CheckState.Unchecked:
            SPN_Select[spn] = 0

    def accept_and_print(self):
        """ Функция вызывается при нажатии на кнопку 'Выбрать' в диалоговом окне.
            Закрывает окно и начинает процесс, составления таблиц данных и
            построение графиков. """

        self.feedback_label.setText("Построение графиков...")
        self.dialog.accept()
        self.draw_graphs()

    def draw_graphs(self):
        self.clear_area()
        try:
            self.widget_tools_layout.removeWidget(self.toolbar)
            self.toolbar.deleteLater()
        except AttributeError:
            pass

        self.fig, self.ax = plt.subplots(figsize=(16, 9))
        sns.set()

        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self.data.iloc[:, -2][0][:8], self.widget_tools)

        count_graph = sum(SPN_Select.values())
        flag_side = True
        index_graph = -1
        combined_df = pd.DataFrame()

        for i, (spn, selected) in enumerate(SPN_Select.items()):
            if selected:
                ''' Получить PGN, обработать position '''
                try:
                    pgn = SPN_PGN[spn]
                    pos = SPN_Position[spn]
                    unit = SPN_Unit[spn]
                    resolution = SPN_Resolution[spn]
                    offset = SPN_Offset[spn]
                    name = SPN_Name[spn]
                    index_graph += 1
                except KeyError:
                    print(f"ERROR: accept_and_print() spn = {spn}")
                    continue

                type_pos, array_pos = descript_position(pos)
                filter_data = filter_data_pgn(self.data, pgn)

                result_data = extract_value(filter_data, type_pos, array_pos).drop_duplicates()
                result_data = result_data.groupby('DateTime').agg(lambda x: x.mode()[0]).reset_index()
                ''' Получили нужные дынные, уходим от битов и переходим к значениям '''
                if resolution is not None:
                    result_data["Value"] *= resolution
                if offset is not None:
                    result_data["Value"] += offset
                # +----------+-------+
                # | DateTime | Value |
                # +----------+-------+
                if i == 0:
                    ''' Создание основного графа '''
                    sns.lineplot(x=result_data['DateTime'],
                                 y=result_data['Value'],
                                 ax=self.ax,
                                 label=f'{name} ({unit})',
                                 color='C%d' % i,
                                 errorbar=EXTEND_ERRORBAR)
                    self.ax.yaxis.set_label_position("left")
                    self.ax.yaxis.tick_left()
                    self.ax.tick_params(axis='y', colors='C%d' % i, rotation=45)
                    self.ax.legend_.remove()
                    self.ax.set_label(name)
                    y_max, y_min = find_y_lim(result_data, i, count_graph)
                    self.ax.set_ylim(y_min, y_max)
                else:
                    ''' Создание накладываемого графа '''
                    ax_new = self.ax.twinx()
                    sns.lineplot(x=result_data['DateTime'],
                                 y=result_data['Value'], ax=ax_new,
                                 label=f'{name} ({unit})',
                                 color='C%d' % index_graph,
                                 errorbar=EXTEND_ERRORBAR)
                    if flag_side:
                        ax_new.yaxis.set_label_position("right")
                        ax_new.yaxis.tick_right()
                        flag_side = False
                    else:
                        ax_new.yaxis.set_label_position("left")
                        ax_new.yaxis.tick_left()
                        flag_side = True
                    ax_new.tick_params(axis='y', colors='C%d' % index_graph, rotation=45)
                    ax_new.legend_.remove()
                    ax_new.set_label(name)
                    y_max, y_min = find_y_lim(result_data, index_graph, count_graph)
                    ax_new.set_ylim(y_min, y_max)

                AX_Interval[name] = (y_max, y_min)
                result_data = result_data.rename(columns={"Value": name})
                # Если комбинированный DataFrame пустой, просто копируем данные
                if combined_df.empty:
                    combined_df = result_data
                else:
                    # Иначе объединяем по столбцу DateTime
                    combined_df = pd.merge(combined_df, result_data, on="DateTime", how="outer")

        self.ax.set_xlabel('Дата и время', fontsize=10)
        scaler_x = len(combined_df["DateTime"][0]) * 12
        self.ax.xaxis.set_major_locator(MaxNLocator(MainWindow.width()//scaler_x))
        self.toolbar.setData(combined_df)

        for ax in self.fig.axes:
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.grid(visible=True)

        self.fig.tight_layout()

        self.feedback_label.setText("График построен")
        self.areaPlot_layout.addWidget(self.canvas)
        self.widget_tools_layout.addWidget(self.toolbar)
        self.legend_bar()
        self.canvas.draw()

    def clear_area(self):
        """ Очищает виджет полотна от старого графика """
        while self.areaPlot_layout.count():
            child = self.areaPlot_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        while self.legendWidget_layout.count():
            child = self.legendWidget_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def save_plot(self):
        """ Вызывается по нажатию кнопки Сохранить, сохраняет график """
        self.feedback_label.setText("Сохранение...")
        filename, _ = QFileDialog.getSaveFileName(MainWindow, "Сохранить график", "", "PNG (*.png);;PDF (*.pdf);;SVG (*.svg)")
        if filename:
            try:
                self.fig.savefig(filename, dpi=DPI_SAVE)
                self.feedback_label.setText("Успешно сохранено")
            except AttributeError:
                self.feedback_label.setText("График не найден")
                print("ERROR: save_plot()")

    def legend_bar(self):
        self.legend_list = QListWidget()

        list_name = []
        i = 0
        for content, selected in SPN_Select.items():
            if selected:
                line = QListWidgetItem(SPN_Name[content])
                color = QColor(*COLOR_C[f'C{i}'])
                pixmap = QPixmap(10, 10)
                pixmap.fill(color)
                line.setIcon(QIcon(pixmap))
                list_name.append(line)
                i += 1
        for line in list_name[::-1]:
            self.legend_list.addItem(line)
        self.legendWidget_layout.addWidget(self.legend_list)
        self.legend_list.itemSelectionChanged.connect(self.click_legend)

        self.header_descript = QWidget()
        self.header_descript_layout = QHBoxLayout()
        self.header_descript.setLayout(self.header_descript_layout)

        self.title_descript = QLabel(u"Описание SPN")
        self.descript_translate_button = QPushButton(u"Перевести")
        self.descript_translate_button.clicked.connect(self.click_btn_translate)

        self.header_descript_layout.addWidget(self.title_descript)
        self.header_descript_layout.addWidget(self.descript_translate_button)


        self.legendWidget_layout.addWidget(self.header_descript)

        self.legend_scroll_descript = QScrollArea()
        self.legend_descript = QLabel()
        self.legend_descript.setMargin(5)
        self.legend_descript.setStyleSheet("background: 'white'")
        self.legend_scroll_descript.setWidgetResizable(True)

        self.legendWidget_layout.addWidget(self.legend_scroll_descript)
        self.legend_scroll_descript.setWidget(self.legend_descript)

    def click_legend(self):
        self.select_graph = self.legend_list.currentItem().text()
        for ax in self.fig.axes:
            try:
                if self.select_graph not in ax.get_legend_handles_labels()[1][0]:
                    ax.tick_params(axis='y', labelleft=False, labelright=False)
                    ax.grid(visible=False)
                else:
                    ax.tick_params(axis='y', labelleft=True, labelright=True)
                    ax.grid(visible=True)
            except IndexError:
                print("ERROR: ", ax.get_legend_handles_labels())
        try:
            if self.select_graph not in self.ax.get_legend_handles_labels()[1][0]:
                self.ax.grid(axis='x')
        except IndexError:
            pass
        self.legend_descript.setText(SPN_Info[int(self.select_graph[self.select_graph.rfind(' ')+1:])])
        self.fig.canvas.draw()

    def click_btn_translate(self):
        text = self.legend_descript.text()
        if not text:
            return
        if text == 1:
            self.feedback_label.setText(u"Для перевода нужен интернет")
        text_trans = translate_to_russian(text)
        if text == text_trans:
            spn = text[text.find('N')+1:text.find(' ')]
            text_trans = SPN_Info[int(spn)]
        self.legend_descript.setText(text_trans)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = UiMainWindow()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())