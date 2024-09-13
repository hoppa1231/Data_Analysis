
import functools
import operator
import numpy as np

from PySide6 import QtCore, QtGui
from PySide6 import QtWidgets

from matplotlib import cbook
from matplotlib.backend_bases import NavigationToolbar2
from pandas.io.sas.sas_constants import dataset_length

import options
from matplotlib.backends.backend_qt import SubplotToolQt

from extend import (colorize_text,
                    extract_value_message,
                    time_to_seconds,
                    AX_Interval)
from settings import PATH_ICON

_to_int = operator.attrgetter('value')

time_m = 0

class NavigationToolbar(NavigationToolbar2, QtWidgets.QToolBar):
    _message = QtCore.Signal(str)  # Remove once deprecation below elapses.

    toolitems = [(None, None, None, None),
                 ('Home', 'Сбросить изменения', 'home', 'home'),
                 ('Back', 'Назад', 'back', 'back'),
                 ('Forward', 'Вперед', 'forward', 'forward'),
                 (None, None, None, None),
                 ('Pan', 'ЛКМ перемещение, ПКМ растяжение', 'move', 'pan'),
                 ('Zoom', 'Зум прямоугольником', 'zoom_to_rect', 'zoom'),
                 ('Subplots', 'Настройки отступов', 'subplots', 'configure_subplots'),
                 (None, None, None, None),
                 ('Customize', 'Настройки графа', 'customize', 'edit_parameters'),
                 ('Pen', 'Просмотр значений', 'pen', 'pen'),
                 (None, None, None, None)]

    def __init__(self, canvas, start_time, parent=None, coordinates=True):
        """coordinates: should we show the coordinates on the right?"""
        QtWidgets.QToolBar.__init__(self, parent)
        self.setAllowedAreas(QtCore.Qt.ToolBarArea(
            _to_int(QtCore.Qt.ToolBarArea.TopToolBarArea) |
            _to_int(QtCore.Qt.ToolBarArea.BottomToolBarArea)))
        self.coordinates = coordinates
        self._actions = {}  # mapping of toolitem method names to QActions.
        self._subplot_dialog = None
        self.canvas = canvas
        self.data = None

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.addSeparator()
            else:
                slot = getattr(self, callback)
                slot = functools.wraps(slot)(functools.partial(slot))
                slot = QtCore.Slot()(slot)

                a = self.addAction(self._icon(image_file + '.png'),
                                   text, slot)
                self._actions[callback] = a
                if callback in ['zoom', 'pan', 'pen']:
                    a.setCheckable(True)
                if tooltip_text is not None:
                    a.setToolTip(tooltip_text)

        if self.coordinates:
            self.locLabel = QtWidgets.QLabel("", self)
            self.locLabel.setAlignment(QtCore.Qt.AlignmentFlag(
                _to_int(QtCore.Qt.AlignmentFlag.AlignRight) |
                _to_int(QtCore.Qt.AlignmentFlag.AlignVCenter)))

            self.locLabel.setSizePolicy(QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Ignored,
            ))
            labelAction = self.addWidget(self.locLabel)
            labelAction.setVisible(True)

        NavigationToolbar2.__init__(self, canvas)

    def _icon(self, name):
        filename = PATH_ICON + name

        pm = QtGui.QPixmap(filename)
        pm.setDevicePixelRatio(
            self.devicePixelRatioF() or 1)

        return QtGui.QIcon(pm)

    def setData(self, data):
        self.data = data
        self.count_graph = 0
        for i, j in AX_Interval.values():
            self.y_min, self.y_max = i, j
            self.count_graph += 1
        self.interval = abs(self.y_max - self.y_min)
        self.offset = self.interval / self.count_graph

    def pen(self):
        if self._actions['pen'].isChecked():
            # Включаем событие на изменение времени (например, через set_message)
            self.motion_cid = self.canvas.mpl_connect('motion_notify_event', self.update_vline_by_time)
            self.click_cid = self.canvas.mpl_connect('button_press_event', self.fix_vline)
            self.vline = None  # Переменная для хранения текущей вертикальной линии
            self.fixed_lines = []  # Список для хранения всех зафиксированных линий
            self.fixed_annotations = []  # Список для хранения всех зафиксированных аннотаций
        else:
            try:
                # Отключаем событие и удаляем вертикальную линию
                if hasattr(self, 'annotations'):
                    for annotation in self.annotations:
                        annotation.remove()
                self.canvas.mpl_disconnect(self.motion_cid)
                self.canvas.mpl_disconnect(self.click_cid)
                # Удаляем все аннотации и линии
                for annotation in self.fixed_annotations:
                    annotation.remove()
                for line in self.fixed_lines:
                    line.remove()
                if self.vline:
                    self.vline.remove()  # Удаляем вертикальную линию с графика
                    self.vline = None
                self.canvas.draw()
            except:
                pass

    def update_vline_by_time(self, event):
        """Обновление линии по времени"""
        global time_m  # Используем глобальную переменную времени из set_message

        if time_m == "":
            return

        if event.inaxes:
            # Рассчитываем смещение по времени
            time_offset_in_seconds = self.data['DateTime'].tolist().index(time_m)
            if not self.vline:
                # Рисуем вертикальную линию на графике, если её ещё нет
                self.vline = event.inaxes.axvline(x=time_offset_in_seconds, color='red', linestyle='--', linewidth=0.5)

            # Обновляем положение линии по времени
            self.vline.set_xdata([time_offset_in_seconds])
            try:
                if hasattr(self, 'annotations'):
                    for annotation in self.annotations:
                        annotation.remove()
            except:
                pass
            self.annotations = []
            x_nearest, y_nearest = 0, 0
            for i, ax in enumerate(self.data.iloc[1:, 1:]):
                ydata = self.data[ax]

                x_nearest = time_offset_in_seconds
                y_nearest = ydata[time_offset_in_seconds]
                interval = self.data[ax].max()
                relative = y_nearest / interval if interval != 0 else i / self.count_graph
                y_spawn = (i + relative)*self.offset + self.y_min - self.interval

                # Если значение x_nearest достаточно близко к текущему времени
                annotation = event.inaxes.annotate(
                        f'{time_m}, {y_nearest:.2f}',
                        xy=(x_nearest, y_spawn),
                        xytext=(5, -2),  # Смещение текста относительно точки
                        textcoords='offset points',
                        bbox=dict(boxstyle="round,pad=0.2",
                                  edgecolor='C%d'%i,
                                  facecolor="white",
                                  linewidth=0.8),
                        fontsize=10,
                        color='C%d'%i
                    )
                self.annotations.append(annotation)
            # Обновляем график
            self.canvas.draw()

    def fix_vline(self, event):
        """Фиксация линии по клику"""
        if self.vline and event.inaxes:
            # Создаем фиксированную линию на основе временной линии
            fixed_line = event.inaxes.axvline(x=self.vline.get_xdata()[0], color='orange', linestyle='--', linewidth=0.5)
            self.fixed_lines.append(fixed_line)

            # Сохраняем текущие аннотации как фиксированные
            for annotation in self.annotations:
                self.fixed_annotations.append(annotation)

            # Убираем временную линию, чтобы можно было рисовать новую
            self.vline.remove()
            self.vline = None

            # Очищаем временные аннотации
            self.annotations = []

            # Обновляем график
            self.canvas.draw()

    def edit_parameters(self):
        axes = self.canvas.figure.get_axes()
        if not axes:
            QtWidgets.QMessageBox.warning(
                self.canvas.parent(), "Error", "There are no Axes to edit.")
            return
        elif len(axes) == 1:
            ax, = axes
        else:
            titles = [
                ax.get_label() or
                ax.get_title() or
                ax.get_title("left") or
                ax.get_title("right") or
                " - ".join(filter(None, [ax.get_xlabel(), ax.get_ylabel()])) or
                f"<anonymous {type(ax).__name__}>"
                for ax in axes]
            duplicate_titles = [
                title for title in titles if titles.count(title) > 1]
            for i, ax in enumerate(axes):
                if titles[i] in duplicate_titles:
                    titles[i] += f" (id: {id(ax):#x})"  # Deduplicate titles.
            item, ok = QtWidgets.QInputDialog.getItem(
                self.canvas.parent(),
                'Редактирование', 'Выберете график:', titles, 0, False)
            if not ok:
                return
            ax = axes[titles.index(item)]
        options.figure_edit(ax, self)

    def _update_buttons_checked(self):
        # sync button checkstates to match active mode
        if 'pan' in self._actions:
            self._actions['pan'].setChecked(self.mode.name == 'PAN')
        if 'zoom' in self._actions:
            self._actions['zoom'].setChecked(self.mode.name == 'ZOOM')

    def pan(self, *args):
        super().pan(*args)
        self._update_buttons_checked()

    def zoom(self, *args):
        super().zoom(*args)
        self._update_buttons_checked()

    def set_message(self, s):
        global time_m
        self._message.emit(s)
        if self.coordinates:
            if s != "":
                time_m, values = extract_value_message(s)

                val_str = ""
                for i in range(len(values)):
                    val_str += colorize_text(f"C{i}", values[i]) + ' '

                s = f"Значения: {val_str}\tВремя: {time_m}"
            self.locLabel.setText(s)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0
        rect = [int(val) for val in (x0, y0, x1 - x0, y1 - y0)]
        self.canvas.drawRectangle(rect)

    def remove_rubberband(self):
        self.canvas.drawRectangle(None)

    def configure_subplots(self):
        if self._subplot_dialog is None:
            self._subplot_dialog = SubplotToolQt(
                self.canvas.figure, self.canvas.parent())
            self.canvas.mpl_connect(
                "close_event", lambda e: self._subplot_dialog.reject())
        self._subplot_dialog.update_from_current_subplotpars()
        self._subplot_dialog.setModal(True)
        self._subplot_dialog.show()
        return self._subplot_dialog

    def set_history_buttons(self):
        can_backward = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack) - 1
        if 'back' in self._actions:
            self._actions['back'].setEnabled(can_backward)
        if 'forward' in self._actions:
            self._actions['forward'].setEnabled(can_forward)