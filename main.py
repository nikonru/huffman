import math
import sys
import os
import tkinter as tk
from tkinter import messagebox

import huffman


#To build use
#pyinstaller --add-data icon.ico;. --windowed --onefile --noconsole --icon=icon.ico main.py
#and uncomment line below
#icon = os.path.join(sys._MEIPASS,"icon.ico")
#icon = "./icon.ico"
#constants
WIN_SIZE ="400x370"
N_SYMB = 7

P = [0.7,
     0.2,
     0.035,
     0.025,
     0.020,
     0.015,
     0.005]

symbols = [i for i in range(N_SYMB)]


def GenerateCode():
    global code_labels
    global symbols
    global P

    #getting variant
    var = e_Var.get()
    if not var:
        var = 0

    #handling errors
    try:
        var = int(var)
    except:
        tk.messagebox.showerror(title="Ошибка", message="Номер вариаенто целое число от 1 до 25")
        return

    if var < 0 or var > 25:
        tk.messagebox.showerror(title="Ошибка",message="Номер вариаенто целое число от 1 до 25")
        return


    #new probabilities

    P_new=list(P)

    dp = var * 0.0015

    P_new[0] -= dp
    P_new[1] -= dp

    for i in range(2,N_SYMB):
        P_new[i] += 0.2*dp

    #generating Hussman code
    symb_P = []
    for i in range(N_SYMB):
        symb_P.append((symbols[i], P_new[i]))

    codes_dict = huffman.codebook(symb_P)

    # entropy
    H = 0
    for i in codes_dict:
        H += -P_new[i] * math.log2(P_new[i])

    # expected length of the code combination
    Q = 0
    for i in codes_dict:
        Q += P_new[i] * len(codes_dict[i])

    # source redundancy
    k = 1 - H / Q

    # setting values to GUI
    for i in codes_dict:
        P_labels[i].config(text = P_new[i])

    for i in codes_dict:
        code_labels[i].config(text = codes_dict[i])

    l_Q.config(text = "Ожидаема длина символа: " + str(Q))
    l_H.config(text = "Энтропия источника: " + str(H))
    l_k.config(text = "Избыточность источника: " + str(k))


#creating window and GUI
window = tk.Tk()

window.title("Huffman Code")
window.geometry(WIN_SIZE)


l_Var = tk.Label(window, text = "Номер варианта:")
e_Var = tk.Entry(window)

b_generate = tk.Button(window, text = "Generate", command = GenerateCode)

#Placing elements of GUI at their places
l_Var.grid(row=0, column=0, pady=2, sticky=tk.E)
e_Var.grid(row=0, column=1, pady=2)

b_generate.grid(row=1, column=1, pady=2, sticky=tk.W)

#Table
l_symb = tk.Label(window, text = "Символ")
l_P = tk.Label(window, text = "Вероятность")
l_code = tk.Label(window, text = "Кодовая комбинация")

l_symb.grid(row=2, column=0, pady=2, sticky=tk.W)
l_P.grid(row=2, column=1, pady=2, sticky=tk.W)
l_code.grid(row=2, column=2, pady=2, sticky=tk.W)
#symbols
SHIFT = 3
symb_labels =[]
for i in symbols:
    k = tk.Label(window,text=i)
    k.grid(row=i+SHIFT, column=0, pady=2, sticky=tk.W)
    symb_labels.append(k)

#Probabilities
P_labels =[]
for i in symbols:
    k = tk.Label(window,text=P[i])
    k.grid(row=i + SHIFT, column=1, pady=2, sticky=tk.W)
    P_labels.append(k)

#Code combinations
code_labels =[]
for i in symbols:
    k = tk.Label(window)
    k.grid(row=i + SHIFT, column=2, pady=2, sticky=tk.W)
    code_labels.append(k)

#Entropy, expected length, redundancy
l_Q = tk.Label(window)
l_H = tk.Label(window)
l_k = tk.Label(window)

l_Q.grid(row=SHIFT+N_SYMB, column=0, columnspan = 2, pady=2, sticky=tk.W)
l_H.grid(row=SHIFT+N_SYMB + 1, column=0, columnspan = 2, pady=2, sticky=tk.W)
l_k.grid(row=SHIFT+N_SYMB + 2, column=0, columnspan = 2, pady=2, sticky=tk.W)

#first generation
GenerateCode()

l_copyright = tk.Label(window, text = "НГТУ 2021: гр. 18-ССК Макаров Н.В. Парамонов А.С.\nhuffman 0.1.2 by Nick Timkovich")
l_copyright.grid(row=SHIFT+N_SYMB + 3, column=0, columnspan=3, pady=2, sticky=tk.W)

#setting icon
try:
    window.iconbitmap(icon)
except:
    pass

window.mainloop()
#creating window and GUI