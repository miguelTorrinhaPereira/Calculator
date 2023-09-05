from tkinter import *
from math import *
from ciencia_calculadora import processar



def rt(n,p):
    return n ** (1/p)


def unshow_solucion():
    global solucion_shown
    text.delete(1.0,END)
    text.config(bg='black')
    solucion_shown = False


def insert(character,movement):
    if solucion_shown: unshow_solucion()
    text.insert('insert',character)
    if index_history == 0: history[index_history] = text.get(1.0,END)
    if movement != 0: move(movement)


def input_manager(event):
    if event.state == 4:
        if event.keysym == 'c':
            content = text.selection_get()
            calculator.clipboard_clear()
            calculator.clipboard_append(content)
        elif event.keysym == 'v':
            text.insert('insert', calculator.selection_get(selection='CLIPBOARD'))
        elif event.keysym == 'BackSpace':
            clear_every_thing()
    elif event.keysym == 'Return':
        calculate()
        return "break"
    elif event.keysym == 'Tab':
        expand()
        return "break"
    elif event.keysym == 'Escape':
        show_menu()
        return "break"
    elif event.keysym == 'Up':
        history_up()
        return "break"
    elif event.keysym == 'Down':
        history_down()
        return "break"
    elif event.keysym == 'BackSpace':
        clear()
        return "break"
    else:
        insert(event.char, 0)
        return "break"


def calculate():
    global solucion_shown

    if solucion_shown:
        unshow_solucion()
        return

    exprecion = text.get(1.0,END)

    exprecion = exprecion.translate(dict_translate)
    exprecion = exprecion.replace('e','2.718281828459045')
    exprecion = exprecion.replace('π','3.141592653589793')
    exprecion = exprecion.replace('√','sqrt')
    exprecion = exprecion.replace('ln','log')
    exprecion = exprecion.replace('fact','factorial')

    try:
        value = 0
        if calc_func == 0:
            exprecion = exprecion.replace('^','**').replace('[','(').replace(']',')')
            value = eval(exprecion)
        elif calc_func == 1:
            value = processar(exprecion)

        global history,index_history
        solucion_shown = True
        text.config(bg=gray2)

        if index_history != 0:
            history[0] = text.get(1.0,END)
            del(history[index_history])
            index_history = 0
        history = [''] + history

        text.delete(1.0,END)
        text.insert(1.0,value)
    except:
        pass


def change_func(new_func):
    global calc_func,menu_active,menu_tracker
    calc_func = new_func
    menu_active = False
    menu_tracker = False
    menu.place_forget()

def show_menu():
    global menu_tracker,menu_active
    menu.place(x=0,y=0)
    menu_tracker = False
    menu_active = True
    update_display(None)


def update_letters():
    global letter_1,letter_2
    for i in buttons:
        for j in range(3,8):i[j].config(font=(font_buttons,letter_1))
        for j in range(3):i[j].config(font=(font_buttons,letter_2))
    button_expand.config(font=(font_buttons,letter_2))
    button_pi.config(font=(font_buttons,letter_1))
    for i in menu_buttons:
        i.config(font=(font_buttons,letter_1))


def update_display(event):
    global width,height
    if event == None or (event.widget == calculator and (width != event.width or height != event.height)):

        if event != None:
            width = event.width
            height = event.height
        calculator.geometry(f'{width}x{height}')

        text.place(width=width)

        extra = expanded * 3
        # these program worked fine in windows , but i had to make some adjustments in order for it to work in linux (ofset).
        ofset_x,ofset_y = -22 if expanded else -23, -8
        size_x,size_y = int((width - (5+extra)*(bd_buttons*2+4))/(5+extra))+ofset_x  ,int((height - 100 - 5*(bd_buttons*2+4))/5)+ofset_y

        global letter_1,letter_2
        letter_max_y, letter_x= size_y*0.47*0.75, size_x*0.75
        letter_1 = floor(min(letter_x*0.47,letter_max_y))
        letter_2 = floor(min(letter_x*0.39,letter_max_y))

        update_letters()

        for i in range(5):

            for j in range(3-extra,8):
                buttons[i][j].config(width=size_x,height=size_y)
                buttons[i][j].grid(row=i, column=j-3+extra)

        if menu_active:
            size_x_menu = int((width - 2*(bd_buttons*2+4))/2)
            for i in range(2):
                menu_buttons[i].config(width=size_x_menu-23)
                menu_buttons[i].grid(row=0,column=i)


def clear():
    if solucion_shown:
        unshow_solucion()
        return

    decimal = text.index('insert').split('.')[1]
    if decimal == '0':
        pos = f'1.{int(decimal)+1}'
        text.delete('insert',pos)
    else:
        pos = f'1.{int(decimal)-1}'
        text.delete(pos,'insert')

def clear_every_thing():
    if solucion_shown:
        unshow_solucion()
        return
    text.delete(1.0,END)


def move(n):
    if solucion_shown: return
    if n>0:text.mark_set('insert',f'insert+{n}c')
    else:text.mark_set('insert',f'insert{n}c')


def update_history():
    if solucion_shown:unshow_solucion()
    text.delete(1.0,END)
    text.insert(1.0,history[index_history][:-1])

def history_up():
    global index_history
    if index_history<len(history)-1:
        index_history += 1
        update_history()

    global menu_tracker
    if menu_tracker:
        menu_tracker = False

def history_down():
    global index_history
    if index_history>0:
        index_history -= 1
        update_history()
    else:
        global menu_tracker , menu_active
        if menu_tracker and not menu_active:
            show_menu()
        elif not menu_tracker:
            menu_tracker = True

def expand():
    global expanded
    expanded = not expanded
    calculator.minsize(300+(expanded*180),300)

    for i in range(5):
        for j in range(3):
            buttons[i][j].grid_forget()

    update_display(None)


def switch():
    global switched
    if switched:
        button_pi.config(text='π',command=lambda:insert('π',0))
        button_exp.config(text='exp',command=lambda:insert('*10^',0))
        button_abs.config(text='abs',command=lambda:insert('abs[]',-1))
        button_mod.config(text='mod',command=lambda:insert('%',0))
        button_log.config(text='log',command=lambda:insert('log10[]',-1))
        button_10_power.config(text='10^x',command=lambda:insert('10^',0))
        button_nd.config(text='2nd')
        button_sin.config(text='sin',command=lambda:insert('sin[]',-1))
        button_cos.config(text='cos',command=lambda:insert('cos[]',-1))
        button_tan.config(text='tan',command=lambda:insert('tan[]',-1))
        button_ln.config(text='ln',command=lambda:insert('ln[]',-1))
    else:
        button_pi.config(text='e',command=lambda:insert('e',0))
        button_exp.config(text='ceil',command=lambda:insert('ceil[]',-1))
        button_abs.config(text='floor',command=lambda:insert('floor[]',-1))
        button_mod.config(text='n!',command=lambda:insert('fact[]',-1))
        button_log.config(text='logab',command=lambda:insert('log[,]',-2))
        button_10_power.config(text='2^x',command=lambda:insert('2^',0))
        button_nd.config(text='1nd')
        button_sin.config(text='asin',command=lambda:insert('asin[]',-1))
        button_cos.config(text='acos',command=lambda:insert('acos[]',-1))
        button_tan.config(text='atan',command=lambda:insert('atan[]',-1))
        button_ln.config(text='e^x',command=lambda:insert('e^',0))
    switched = not switched





calc_func = 0
menu_tracker = False
menu_active = False
dict_translate = {247:'/',215:'*',8722:'-'}
width = 500
height = 600
switched = False
expanded = False
solucion_shown = False
history = ['']
index_history = 0


calculator = Tk()
calculator.title('Calculadora')
calculator.geometry('500x600')
calculator.configure(bg='black')
calculator.minsize(300,300)


text = Text(calculator,wrap=WORD,bd=2,bg='black',fg='white',insertbackground='white',font=('Arial',25))
text.place(x=0,y=0,width=500,height=100)
text.focus_set()

text.bind('<Key>', input_manager)


buttons = []
size_x, size_y = 73,88

letter_1 = 30
letter_2 = 25
font_buttons = 'Helvetica'
bd_buttons = 0
white = '#DDDDDD'
red = '#FF0000'
orange = '#FF8000'
gray1 = '#333333'
gray2 = '#1D1D1D'
gray3 = '#111111'
pixel = PhotoImage(width=1,height=1)


button_frame = Frame(calculator,bg=gray3)
button_frame.place(x=0,y=100)


button_expand = Button(button_frame, text='EXP', fg=white,bg=gray3, command=expand, font=(font_buttons, letter_2), bd=bd_buttons, image=pixel,width=size_x, height=size_y, compound='center')
button_left_brace = Button(button_frame, text='(',fg=white, bg=gray2, command=lambda:insert('(',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_right_brace = Button(button_frame, text=')',fg=white, bg=gray2, command=lambda:insert(')',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_ce = Button(button_frame, text='CE',fg=white, bg=red, command=clear_every_thing, font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_c = Button(button_frame, text='C',fg=white, bg=red, command=clear, font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')

button_7 = Button(button_frame, text='7',fg=white, bg=gray1, command=lambda:insert('7',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_8 = Button(button_frame, text='8',fg=white, bg=gray1, command=lambda:insert('8',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_9 = Button(button_frame, text='9',fg=white, bg=gray1, command=lambda:insert('9',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_plus = Button(button_frame, text='+',fg=white, bg=orange, command=lambda:insert('+',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_left_arrow = Button(button_frame, text='←',fg=white, bg=gray3, command=lambda:move(-1), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')

button_4 = Button(button_frame, text='4',fg=white, bg=gray1, command=lambda:insert('4',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_5 = Button(button_frame, text='5',fg=white, bg=gray1, command=lambda:insert('5',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_6 = Button(button_frame, text='6',fg=white, bg=gray1, command=lambda:insert('6',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_minus = Button(button_frame, text='−',fg=white, bg=orange, command=lambda:insert('−',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_right_arrow = Button(button_frame, text='→',fg=white, bg=gray3, command=lambda:move(1), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')

button_1 = Button(button_frame, text='1',fg=white, bg=gray1, command=lambda:insert('1',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_2 = Button(button_frame, text='2',fg=white, bg=gray1, command=lambda:insert('2',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_3 = Button(button_frame, text='3',fg=white, bg=gray1, command=lambda:insert('3',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_mult = Button(button_frame, text='×',fg=white, bg=orange, command=lambda:insert('×',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_up_arrow = Button(button_frame, text='↑',fg=white, bg=gray3, command=history_up, font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')

button_dot = Button(button_frame, text='.',fg=white, bg=gray2, command=lambda:insert('.',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_0 = Button(button_frame, text='0',fg=white, bg=gray1, command=lambda:insert('0',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_equals = Button(button_frame, text='=',fg=white, bg=orange, command=calculate, font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_div = Button(button_frame, text='÷',fg=white, bg=orange, command=lambda:insert('÷',0), font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')
button_down_arrow = Button(button_frame, text='↓',fg=white, bg=gray3,command=history_down, font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y, compound='center')



button_squared = Button(button_frame, text='x^2',fg=white, bg=gray2,command=lambda:insert('^2',0) ,font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_power = Button(button_frame, text='x^y',fg=white, bg=gray2,command=lambda:insert('^',0) ,font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_square_root = Button(button_frame, text='√',fg=white, bg=gray2,command=lambda:insert('√[]',-1) , font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_root = Button(button_frame, text='rt',fg=white, bg=gray2,command=lambda:insert('rt[,]',-2) ,font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_pi = Button(button_frame, text='π',fg=white, bg=gray2,command=lambda:insert('π',0) , font=(font_buttons, letter_1), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')

button_exp = Button(button_frame, text='exp',fg=white, bg=gray2,command=lambda:insert('*10^',0) ,font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_abs = Button(button_frame, text='abs',fg=white, bg=gray2,command=lambda:insert('abs[]',-1) , font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_mod = Button(button_frame, text='mod',fg=white, bg=gray2,command=lambda:insert('%',0) , font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_log = Button(button_frame, text='log',fg=white, bg=gray2,command=lambda:insert('log10[]',-1) ,font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_10_power = Button(button_frame, text='10^x',fg=white,command=lambda:insert('10^',0) ,bg=gray2, font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')

button_nd = Button(button_frame, text='2nd',fg=white, bg=gray3, command=switch, font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_sin = Button(button_frame, text='sin',fg=white, bg=gray2,command=lambda:insert('sin[]',-1), font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_cos = Button(button_frame, text='cos',fg=white, bg=gray2,command=lambda:insert('cos[]',-1), font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_tan = Button(button_frame, text='tan',fg=white, bg=gray2,command=lambda:insert('tan[]',-1), font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')
button_ln = Button(button_frame, text='ln',fg=white, bg=gray2,command=lambda:insert('ln[]',-1), font=(font_buttons, letter_2), bd=bd_buttons, image=pixel, width=size_x, height=size_y,  compound='center')


buttons += [[button_nd, button_exp, button_squared, button_expand, button_left_brace, button_right_brace, button_ce, button_c],
           [button_sin,button_abs,button_power,button_7,button_8,button_9,button_plus,button_right_arrow],
           [button_cos,button_mod,button_square_root,button_4,button_5,button_6,button_minus,button_left_arrow],
           [button_tan,button_log,button_root,button_1,button_2,button_3,button_mult,button_up_arrow],
           [button_ln,button_10_power,button_pi,button_dot,button_0,button_equals,button_div,button_down_arrow]]


for i in range(5):
    for j in range(3,8):
        buttons[i][j].grid(row=i,column=j-3)


menu = Frame(calculator)


button_mode_normal = Button(menu,text='normal',fg=white,bg=gray3,command=lambda:change_func(0), font=(font_buttons,letter_1),bd=bd_buttons, image=pixel,width=236, height=86,compound='center')
button_mode_ciencia = Button(menu,text='ciência',fg=white,bg=gray3,command=lambda:change_func(1), font=(font_buttons,letter_1),bd=bd_buttons, image=pixel,width=236,height=86, compound='center')


menu_buttons = [button_mode_normal,button_mode_ciencia]


calculator.bind('<Configure>',update_display)


calculator.mainloop()