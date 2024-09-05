import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

# Создаем график
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5])

# Создаем вертикальную линию
vline = ax.axvline(x=0, color='red')

# Создаем окно с координатами точки
annot = ax.annotate('', xy=(0, 0), xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round', fc='0.8'), arrowprops=dict(arrowstyle='->'))

# Функция, которая обновляет положение вертикальной линии и окна с координатами точки
def update(event):
    if event.inaxes == ax:
        x = event.xdata
        if x is not None:
            vline.set_xdata([x])
            annot.xy = (x, event.ydata)
            annot.set_text(f'({x:.2f}, {event.ydata:.2f})')
            fig.canvas.draw_idle()

# Функция, которая фиксирует положение вертикальной линии и окна с координатами точки при клике
def click(event):
    if event.inaxes == ax:
        x = event.xdata
        y = event.ydata
        vline.set_xdata([x])
        annot.xy = (x, y)
        annot.set_text(f'({x:.2f}, {y:.2f})')
        fig.canvas.draw_idle()
        print(f'Клик по точке ({x:.2f}, {y:.2f})')

# Подключаем функции к событиям мыши
fig.canvas.mpl_connect('motion_notify_event', update)
fig.canvas.mpl_connect('button_press_event', click)

plt.show()