import tkinter
from cgitb import text
from tkinter import *
from tkinter import messagebox

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.pyplot import Figure
import random
from matplotlib import style


# import PIL

# IMAGETEXT

window = Tk()
window.geometry("1300x600")
window.title("Symulator układu RLC")
style.use("ggplot")

# my_canvas = Canvas(window, width=600, height=800, background='gray')
# my_canvas.pack(fill='both', expand='true')

icon = PhotoImage(file="koła.gif")
window.iconphoto(True, icon)

window.config(background="gray")
photo = PhotoImage(file='układ.gif')

# class parameters:
#     def __init__(self, amplitude, freq, step, end_time, signal_type, duty, impulse_num, R2, R1, C):
#         self.amplitude = amplitude
#         self.freq = freq
#         self.step = step
#         self.end_time = end_time
#         self.signal_type = signal_type
#         self.duty = duty
#         self.impulse_num = impulse_num
#         self.R2 = R2
#         self.R1 = R1
#         self.C = C

# p1 = parameters (1,1,0.001,10,3,0.5,10,5,10,0.001)

amplitude = 1
freq = 1
step = 0.001
end_time = 10
signal_type = 3
duty = 0.5
impulse_num = 10
R2 = 5
R1 = 10
C = 0.001

input_tab = []
output_tab = []
time_tab = []


def count():
    # if isinstance(textfield[0].get("1.0",END),int):
    #    print("Write a number")
    # else:
    #    R1 = int(textfield[0].get("1.0",END))
    #   print(R1)

    fill_time_tab()
    fill_input_tab(2)
    fill_output_tab()
    plot()


RLC = Label(window,
            relief=SOLID,
            image=photo,
            compound='right')

words = [0, 1, 2, 3]
textfield = [0, 1, 2, 3]

textfield[0] = Text(window,
                    font=('New Times Roman', 10),
                    height=1,
                    width=20)

textfield[1] = Text(window,
                    font=('New Times Roman', 10),
                    height=1,
                    width=20)

textfield[2] = Text(window,
                    font=('New Times Roman', 10),
                    height=1,
                    width=20)

textfield[3] = Text(window,
                    font=('New Times Roman', 10),
                    height=1,
                    width=20)

words[0] = Label(window,
                 text='R1 = ',
                 bg='grey',
                 font=("New Times Roman", 11, 'bold'))

words[1] = Label(window,
                 text='R2 = ',
                 bg='grey',
                 font=("New Times Roman", 11, 'bold'))

words[2] = Label(window,
                 text='C = ',
                 bg='grey',
                 font=("New Times Roman", 11, 'bold'))

words[3] = Label(window,
                 text='L = ',
                 bg='grey',
                 font=("New Times Roman", 11, 'bold'))

button = Button(window,
                text='Oblicz',
                command=count,
                font=("New Times Roman", 10, 'bold'),
                relief=SOLID,
                bd=3)

# entry = Entry(window,
#                 font=('Arial',10,'bold'))
for i in range(4):
    words[i].place(x=15, y=240 + 30 * i)

for i in range(4):
    textfield[i].place(x=60, y=240 + 30 * i)

RLC.place(x=20, y=20)
button.place(x=600, y=20)


# R1.place(x=15, y=240)
# R2.place(x=15, y=270)
# C.place(x=15, y=300)
# L.place(x=15, y=330)

# R1_text.place(x=60, y=240)
# R2_text.place(x=60, y=270)
# L_text.place(x=60, y=300)
# C_text.place(x=60, y=330)

# entry.pack(side=BOTTOM)


def square_sig(t):
    if(t<(1/freq)*impulse_num):
        if (t%(1/freq)<duty*(1/freq)):
            sig = amplitude
        else:
            sig = 0
    else:
        sig =0
    return sig


def sin_sig(t):
    sig = amplitude * np.sin(2 * np.pi * freq * t)
    return sig


def triang_sig(t):
    if (t % (1 / freq) < 0.5 * (1 / freq)):
        sig = amplitude*((t % (0.5*(1/freq))) / 0.5*(1/freq))
    else:
        sig = amplitude - amplitude*((t % (0.5*(1/freq))) / 0.5*(1/freq))
    return sig


def fill_time_tab():
    t = 0
    while t <= end_time:
        time_tab.append(t)
        t += step


def fill_input_tab(type):
    match type:
        case 1:
            for t in time_tab:
                input_tab.append(square_sig(t))
        case 2:
            for t in time_tab:
                input_tab.append(sin_sig(t))
        case 3:
            for t in time_tab:
                input_tab.append(triang_sig(t))

def fill_output_tab():
    ur = 0.0
    for u1 in input_tab:
        ur = ur + step * (u1 - ur*(1+(R2/R1))/C*R2)
        output_tab.append(ur)



def plot():
    print("working")

    # plt = plt.plot(time_tab, output_tab)
    charts = Frame()
    charts.place(x=750, y=70)
    # create figure
    fig = Figure(figsize=(5,5), dpi=100, facecolor="gray")
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(212)

    # ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
    # ax2 = plt.subplot2grid((6, 1), (0, 0), rowspan=3, colspan=1)
    # ax3 = plt.subplot2grid((6, 1), (0, 0), rowspan=4, colspan=1)

    xs=[]
    ys=[]

    for i in range(10):
         x=i
         y=random.randrange(10)

    xs.append(x)
    ys.append(y)


    ax1.plot(x,y)
    ax2.plot(time_tab, output_tab)
    ax3.plot(time_tab, output_tab)

    # create matplotlib canvas using `fig` and assign to widget `top`
    canvas = FigureCanvasTkAgg(fig, charts)

    # get canvas as tkinter widget and put in widget `top`
    canvas.get_tk_widget().pack()

    # create toolbar
    # toolbar = NavigationToolbar2TkAgg(canvas, charts)
    # toolbar.update()
    # canvas._tkcanvas.pack()

    # --- first plot ---

    # create first place for plot
    # ax1 = fig.add_subplot(211)

    # draw on this plot
    # plt.plot(kind='bar', legend=False, ax=ax1)


    # f = Figure(figsize=(5, 5), dpi=100)
    # a = f.add_subplot(111)
    # a.plot([1,10], [8,20])
    # # a.plot(time_tab, output_tab)
    #
    # my_canvas = FigureCanvasTkAgg(f, window)
    # my_canvas.draw()
    # my_canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=TRUE)

    # wykres = plt.plot(time_tab, output_tab)
    # wykres_window = my_canvas.create_window(34, 290, anchor='nw', window=wykres)
    # plt.show()





window.mainloop()
