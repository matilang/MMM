import math
import tkinter
from cgitb import text
from tkinter import *
from tkinter import messagebox

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from numpy import double
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
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

amplitude = 1
freq = 1
step = 0.001
end_time = 4
# signal_type = 1
duty = 1
impulse_num = 1
R2 = 5
R1 = 10
C = 1

param = [0,1,2,3,4,5,6,7,8,9]
param[0] = "R1"
param[1] = "R2"
param[2] = "C"
param[3] = 'amplitude'
param[4] = 'freq'
param[5] = 'step'
param[6] = 'end_time'
param[7] = 'duty'
param[8] = 'impulse_num'


input_tab = []
output_tab = []
time_tab = []
pulse_tab = []
bode_amplitude_tab = []
bode_phase_tab = []
bode_bounds = {-500, 500}

# class param:
#
#     def __init__(self,R1):
#         self.R1 = 10
def uwaga():
    messagebox.showerror(title='Uwaga', message='Jedno z okien jest nie wypełnione')

def count():

    my_label.config(text=wybor_syg.get(ANCHOR))
    text = wybor_syg.get(ANCHOR)
    if (text=='Sygnał prostokątny'):
        signal_type=1
    elif (text=='Sygnał sinusoidalny'):
        signal_type=2
    else:
        signal_type=3

    param = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # param[0] = R1
    # param[1] = R2
    # param[2] = C
    # param[3] = amplitude
    # param[4] = freq
    # param[5] = step
    # param[6] = end_time
    # param[7] = duty
    # param[8] = impulse_num
    for i in range (9):
        # while True:
        #     try:
        #         par = int(textfield[i].get("1.0", END))
        #     except ValueError:
        #         messagebox.showerror(message="nie liczba")

        param[i] = textfield[i].get("1.0",END)
        if ((len(param[i])-1) == 0):
          uwaga()
          break
        else:
            param[i] = float(param[i])

    for k in range(8):
        print(param[k])
    print('koniec')

    clear_tabs()
    fill_time_tab(param[5],param[6])
    fill_input_tab(signal_type,param[4],param[3],param[7],param[8])
    fill_output_tab(param[0],param[1],param[2],param[5])
    fill_pulse_tab()
    fill_bode_phase_tab(param[0],param[1],param[2])
    fill_bode_amplitude_tab(param[0],param[1],param[2])
    plot()


RLC = Label(window,
            relief=SOLID,
            image=photo,
            compound='right')

words = [0,1,2,3,4,5,6,7,8]
textfield = [0,1,2,3,4,5,6,7,8]

for i in range(9):
    textfield[i] = Text(window,
                    font=('New Times Roman', 10),
                    height=1,
                    width=20)
    words[i] = Label(window,
                 text=(''+ str(param[i]) +" = "),
                 bg='grey',
                 font=("New Times Roman", 11, 'bold'))

button = Button(window,
                text='Oblicz',
                command=count,
                font=("New Times Roman", 10, 'bold'),
                relief=SOLID,
                bd=3)

wybor_syg = Listbox(window, height=3)

wybor_syg.insert(0,"Sygnał prostokątny")
wybor_syg.insert(1,"Sygnał sinusoidalny")
wybor_syg.insert(2,"Sygnał trójkątny")

global my_label
my_label = Label(window, text='Sygnał trójkątny', background="gray")
# entry = Entry(window,
#                 font=('Arial',10,'bold'))
for i in range(9):
    words[i].place(x=15, y=240 + 30 * i)
    textfield[i].place(x=140, y=240 + 30 * i)

del param

RLC.place(x=20, y=20)
button.place(x=580, y=20)
wybor_syg.place(x=550, y=60)
my_label.place(x=550, y=120)


def square_sig(t,freq,amplitude,duty,impulse_num):
    if(t<(1/freq)*impulse_num):
        if (t%(1/freq)<duty*(1/freq)):
            sig = amplitude
        else:
            sig = 0
    else:
        sig =0
    return sig


def sin_sig(t,freq,amplitude):
    sig = amplitude * np.sin(2 * np.pi * freq * t)
    return sig


def triang_sig(t,freq,amplitude):
    if (t % (1 / freq) < 0.5 * (1 / freq)):
        sig = amplitude*((t % (0.5*(1/freq))) / 0.5*(1/freq))
    else:
        sig = amplitude - amplitude*((t % (0.5*(1/freq))) / 0.5*(1/freq))
    return sig


def fill_time_tab(step,end_time):
    t = 0
    while t <= end_time:
        time_tab.append(t)
        t += step


def fill_input_tab(type,freq,amplitude,duty,impulse_num):
    match type:
        case 1:
            for t in time_tab:
                input_tab.append(square_sig(t,freq,amplitude,duty,impulse_num))
        case 2:
            for t in time_tab:
                input_tab.append(sin_sig(t,freq,amplitude))
        case 3:
            for t in time_tab:
                input_tab.append(triang_sig(t,freq,amplitude))
def extend_input_tab(type, start, stop, step2, extended_input_tab,freq,amplitude,duty):
    t = start
    stop =int( (stop - start)/step2)
    match type:
        case 1:
            for i in range(0, stop):
                t += step2
                extended_input_tab.append(square_sig(t,freq,amplitude,duty))
        case 2:
            for t in range(0, stop):
                t += step2
                extended_input_tab.append(sin_sig(t,freq,amplitude,duty))
        case 3:
            for t in range(0, stop):
                t += step2
                extended_input_tab.append(triang_sig(t,freq,amplitude,duty))

def fill_output_tab(R1,R2,C,step):
    ur = 0.0

    for i in range(0, time_tab.__len__()) :
        u1 = input_tab[i]
        output_tab.append(ur)

        diff = u1/C - ((1+(R2/R1))/C)*ur
        ur = ur + step*diff




        # if(i<400):
        #     print(time_tab[i])
        #     print(u1)
        #     print(ur)
        #     print(diff)
        #     print("    ,     ")

def fill_pulse_tab():
    for i in range ( -200, 200):
        pulse_tab.append(pow(1.2, i))


def fill_bode_amplitude_tab(R1,R2,C):
    for w in pulse_tab:
        a = 1/math.sqrt(pow((1 + R2/R1), 2)+pow(C*w, 2))
        a_dB = 20*math.log(a, 10)
        bode_amplitude_tab.append(a_dB)
        # print(str(w) + "         " + str(a_dB))

def fill_bode_phase_tab(R1,R2,C):
    for w in pulse_tab:
        phi = math.atan2(0, 1) - math.atan2(C*w, (1 + R2/R1))
        bode_phase_tab.append(phi)


def clear_tabs():
    time_tab.clear()
    output_tab.clear()
    input_tab.clear()
    pulse_tab.clear()
    bode_amplitude_tab.clear()
    bode_phase_tab.clear()

def plot():
    print("working")

    # plt = plt.plot(time_tab, output_tab)
    charts = Frame()
    charts.place(x=700, y=0)
    # create figure
    fig = Figure(figsize=(6,6), dpi=100, facecolor="gray")
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)


    ax1.plot(time_tab, input_tab)
    ax2.plot(time_tab, output_tab)
    ax3.plot(pulse_tab, bode_amplitude_tab)
    ax4.plot(pulse_tab, bode_phase_tab)
    ax3.set_xscale('log')
    ax4.set_xscale('log')

    # create matplotlib canvas using `fig` and assign to widget `top`
    canvas = FigureCanvasTkAgg(fig, charts)

    # get canvas as tkinter widget and put in widget `top`
    canvas.get_tk_widget().pack()

    # create toolbar
    # toolbar = NavigationToolbar2TkAgg(canvas, charts)
    # toolbar.update()
    # canvas._tkcanvas.pack()


window.mainloop()
