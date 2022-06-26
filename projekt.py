import math
from tkinter import *
from tkinter import messagebox

import numpy as np
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure

window = Tk()
window.geometry("1300x600")
window.title("Symulator układu RLC")
style.use("ggplot")


icon = PhotoImage(file="koła.gif")
window.iconphoto(True, icon)

window.config(background="gray")
photo = PhotoImage(file='układ.gif')


param = [0,1,2,3,4,5,6,7,8,9]
param[0] = "R1 [Ω]"
param[1] = "R2 [Ω]"
param[2] = "C [F]"
param[3] = 'Amplituda [V]'
param[4] = 'Częstotliwość [Hz]'
param[5] = 'Krok symulacji'
param[6] = 'Dlugość symulacji'
param[7] = 'Wsp. wypełnienia'
param[8] = 'Ilość impulsów'


input_tab = []
output_tab = []
time_tab = []
pulse_tab = []
bode_amplitude_tab = []
bode_phase_tab = []
bode_bounds = {-500, 500}
signal_type=1


def uwaga():
    messagebox.showerror(title='Uwaga', message='Jedno z okien jest nie wypełnione')

def digit(strin):

        strin = strin[:-1]

        t = len(strin)

        x=0
        y=0
        z=0

        for i in range(t):
            if strin[i].isnumeric():
                y = y+1;
            elif (strin[i] == '.') and (x == 0):
                x = x+1
            else:
                z = z+1
        if ((y > 0) and (x < 2) and (z == 0)):
            return TRUE
        else:
            return FALSE



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

        param[i] = textfield[i].get("1.0",END)
        strin = textfield[i].get("1.0",END)
        if (digit(strin) == FALSE):
            messagebox.showerror(message="Zła liczba lub puste pole")
            break
        if ((len(param[i])-1) == 0):
          uwaga()
          break
        else:
            param[i] = float(param[i])

    clear_tabs()
    fill_time_tab(param[5],param[6])
    fill_input_tab(signal_type,param[4],param[3],param[7],param[8])
    fill_output_tab(param[0],param[1],param[2],param[5])
    # time_analysis(param[0],param[1], param[2], param[5], signal_type, param[4], param[3], param[7], param[8], param[6])
    fill_pulse_tab()
    fill_bode_phase_tab(param[0],param[1],param[2])
    fill_bode_amplitude_tab(param[0],param[1],param[2])
    plot()
    del param


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

# resist = ["mΩ","Ω", "kΩ","MΩ"]
# x=IntVar()
# x2=IntVar()
# for index in range(len(resist)):
#         radiobutton = Radiobutton(window,  variable=x, value=index, text=resist[index])
#         radiobutton.place(x=320 + 60 * index, y=240)
#
# for index in range(len(resist)):
#         radiobutton = Radiobutton(window,  variable=x2, value=index, text=resist[index])
#         radiobutton.place(x=320 + 60 * index, y=270)
#
# y=IntVar()
# farad = ["mF", "F", "kF", "MF"]
# for index in range(len(farad)):
#     radiobutton = Radiobutton(window,  variable=y, value=index, text=farad[index])
#     radiobutton.place(x=320 + 60 * index, y=300)
# z=IntVar()
# amp = ["mV", "V", "kV", "MV"]
# for index in range(len(amp)):
#     radiobutton = Radiobutton(window,  variable=z, value=index, text=amp[index])
#     radiobutton.place(x=320 + 60 * index, y=330)
# k=IntVar()
# fre = ["mHz", "Hz", "kHz", "MHz"]
# for index in range(len(fre)):
#     radiobutton = Radiobutton(window,  variable=k, value=index, text=fre[index])
#     radiobutton.place(x=320 + 60 * index, y=360)

wybor_syg = Listbox(window, height=3)
wybor_syg.insert(0,"Sygnał prostokątny")
wybor_syg.insert(1,"Sygnał sinusoidalny")
wybor_syg.insert(2,"Sygnał trójkątny")

global my_label
my_label = Label(window, text='Sygnał trójkątny', background="gray")

for i in range(9):
    words[i].place(x=15, y=240 + 30 * i)
    textfield[i].place(x=170, y=240 + 30 * i)

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


def fill_output_tab(R1,R2,C,step):
    ur = 0.0

    for u1 in input_tab :
        # u1 = input_tab[i]
        output_tab.append(ur)

        diff = u1/(C*R2) - ((R1+R2)/(R1*R2*C))*ur

        ur = ur + step * diff



        print(u1)
        print(ur)
        print(diff)
        print("      ,    ")




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


    charts = Frame()
    charts.place(x=700, y=0)
    # create figure
    fig = Figure(figsize=(6,6), dpi=100, facecolor="gray", )
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

    ax1.set_title('Sygnał wejściowy', fontdict={'fontsize': 10})
    ax2.set_title('Sygnał wyjściowy', fontdict={'fontsize': 10})
    ax3.set_title('Wykres amplitudowy Bodego', fontdict={'fontsize': 10})
    ax4.set_title('Wykres fazowy Bodego', fontdict={'fontsize': 10})

    canvas = FigureCanvasTkAgg(fig, charts)
    canvas.get_tk_widget().pack()


window.mainloop()
