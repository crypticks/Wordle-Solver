#                                               INSTRUCTIONS FOR USE

# The input system is similar to that of Wordle itself. After typing out the word, you can click on each box to change the colour of it, as seen in the Wordle game. Pressing enter inputs this data and shows all possible words to the left of the input boxes.
# 
# The green word at the top is the best recommended word as the next input. Yellow words are fairly good, and white words are... normal i guess? 
# 
# Instead of typing out the word from the list, you can also simply click on it and it gets autofilled. Your input history is stored on the right side. The window also has a Quit button on the Top Left side and a Reset button on the Bottom Right, in case you mess up any of the inputs, or get tired of how good this program is (*wink*)

#PS: The following packages are needed:

from collections import Counter
from pynput.keyboard import Key, Listener
import pygetwindow as pgw
from pynput import mouse
import time
from tkinter import ttk
import tkinter as tk



#COLOURS
gray = '#222222'
green = '#019a01'
yellow = '#ffc425'
backgroundcolor = '#111111'

#FUNCTIONAL VARIABLES
z=0
arr = [""]*50
for ele in arr:
    ele = "!"
i=1
x = 0
a = [""]*12972
flags = [0]*12972
turn = 1
m=1
t = 1
finish = 0

#UI
root = tk.Tk()
root.title("Wordle Solver")
root.geometry("1920x1080")
root.configure(background=backgroundcolor)
frame = tk.Frame(root)
frame.pack()




def load_file_into_array(): #READS THE TEXT FILE AND MAKES ARRAY OF WORDS
    global x
    file = open('combined_wordlist.txt')
    lines = file.readlines()
    for line in lines:
        a[x]=line.upper()
        x+=1
    
    x=0
    file.close()


                      
def autofill(): # FILLS IN THE WORD CLICKED ON, IN THE LISTBOX
    global z,m
    if z!=0:
        time.sleep(0.1)
        try:
            selected = all.get(all.curselection()[0], all.curselection()[0])[0]
            btn1.configure(text = selected[0])
            btn2.configure(text = selected[1])
            btn3.configure(text = selected[2])
            btn4.configure(text = selected[3])
            btn5.configure(text = selected[4])
            z=0
            m=6
        except IndexError:
            return
    else: z=1



def compute(): #FILTER SYSTEM BASED ON GREENS, YELLOWS AND GRAYS
    print("computing")
    global x
    i = 0
    while i<12972:
        if flags[i]!=1:
            m=0
            while m<x:
                s = a[i]

                # GREEN CHECK
            
                if arr[m][2] == 'g':
                    if s[int(arr[m][1])-1]!=arr[m][0]:
                        flags[i] = 1
                        break

                
                # YELLOW CHECK

                if arr[m][2] == 'y' and flags[i]!=1:
                    if arr[m][0]==s[int(arr[m][1])-1]:
                        flags[i]=1
                        break

                    if s.find(arr[m][0]) ==-1:
                        flags[i]=1
                        break

                # GRAY CHECK
                
                if arr[m][2] == 'x' and flags[i]!=1:
                    count=0
                    pos = 10
                    for k in range(0,m):
                        if arr[k][0]==arr[m][0]:
                            count+=1
                            break
                    if count>0:
                        if Counter(s)[arr[m][0]] > count:
                            flags[i]=1
                            break

                    elif(s.find(arr[m][0])!=-1):
                        flags[i] = 1
                        break

                m+=1
        i+=1


def recommend():

    #DECIDES PRIORITY ORDER IN 2 STEPS. THE 1 TOP RECOMMENDED WORD RELIES ON HOW LIKELY EACH INDIVIDUAL LETTER IS TO BE PRESENT IN THE WORD, BASED ON STATISTICS. OTHER RECOMMENDED WORDS RELY ON HOW DIVERSE ITS CHARACTER SET IS.

    maxi = 0
    pos = 0
    for i in range(0,12972):
        if int(flags[i])==1: continue
        if(len(Counter(a[i]))>=maxi):
            if(len(Counter(a[i])) > maxi):
                pos =0

            flags[i] = 2
            pos+=1
            maxi=len(Counter(a[i]))

    priority = ['Q', 'X', 'J', 'Z', 'V', 'W', 'F', 'K', 'G', 'B', 'H', 'P', 'M', 'Y', 'C', 'D', 'U', 'N', 'T', 'L', 'I', 'R', 'O', 'S', 'E', 'A']
    pindexes = [0]*12972

    for i in range(0, 12972):
        if int(flags[i]==0 or flags[i]==1): pindexes[i]=0
        else:
            pindexes[i] = priority.index(a[i][0]) + priority.index(a[i][1]) + priority.index(a[i][2]) + priority.index(a[i][3]) + priority.index(a[i][4])

    flags[pindexes.index(max(pindexes))] = 3




def btncon(button): # CYCLES THROUGH COLOURS FOR INPUT BOXES
    c = button.cget('bg')
    if(c == gray): button.configure(bg = green)
    elif(c == green): button.configure(bg = yellow)
    elif(c == yellow): button.configure(bg = gray)


def on_click(x, y, button, pressed):
    if(x>370 and x < 680): # DETECTING CLICK ON WORDLIST
        autofill()


def on_press(key):
    windowname = pgw.getActiveWindowTitle()
    global finish, turn, m, x
      
    if windowname == "Wordle Solver": #prevents data being input while the wordle site is being used
        if turn < 7 and finish == 0:            
            if key == Key.alt_r or key == Key.tab or key == Key.shift or key == Key.alt_l or key == Key.ctrl_l or key == Key.ctrl_r: return #skips special keys that interfere with input eg. while switching tabs

            if key==Key.enter and m<6: return


            if key==Key.enter and m == 6:
                col = ''
                if btn1.cget('bg')==green and btn2.cget('bg')==green and btn3.cget('bg')==green and btn4.cget('bg')==green and btn5.cget('bg')==green:
                    finishtext.configure(text = 'WORD FOUND')
                    finishtext.place(x=660, y = 150)    #GAME END SUCCESS
                    finish = 1


                else:
                    #READING INPUT TO ARRAY
                    if btn1.cget('bg') == green:
                        col = 'g'
                    elif btn1.cget('bg') == gray:   
                        col = 'x'
                    elif btn1.cget('bg') == yellow:
                        col = 'y'
                    arr[x] = btn1.cget('text') + '1' + col
                    x+=1

                    if btn2.cget('bg') == green:
                        col = 'g'
                    elif btn2.cget('bg') == gray:   
                        col = 'x'
                    elif btn2.cget('bg') == yellow:
                        col = 'y'
                    arr[x] = btn2.cget('text') + '2' + col
                    x+=1

                    if btn3.cget('bg') == green:
                        col = 'g'
                    elif btn3.cget('bg') == gray:   
                        col = 'x'
                    elif btn3.cget('bg') == yellow:
                        col = 'y'
                    arr[x] = btn3.cget('text') + '3' + col
                    x+=1

                    if btn4.cget('bg') == green:
                        col = 'g'
                    elif btn4.cget('bg') == gray:   
                        col = 'x'
                    elif btn4.cget('bg') == yellow:
                        col = 'y'
                    arr[x] = btn4.cget('text') + '4' + col
                    x+=1

                    if btn5.cget('bg') == green:
                        col = 'g'
                    elif btn5.cget('bg') == gray:   
                        col = 'x'
                    elif btn5.cget('bg') == yellow:
                        col = 'y'
                    arr[x] = btn5.cget('text') + '5' + col
                    x+=1


                    compute()
                    recommend()

                    #OUTPUT TO HISTORY (MID RIGHT)
                    all.delete('0','end')
                    
                    prev.insert('end', btn1.cget('text') + btn2.cget('text') + btn3.cget('text') + btn4.cget('text') + btn5.cget('text'))

                    #CLEARS INPUT FIELD
                    btn1.configure(text = '')
                    btn2.configure(text = '')
                    btn3.configure(text = '')
                    btn4.configure(text = '')
                    btn5.configure(text = '')

                    btn1.configure(bg = gray)
                    btn2.configure(bg = gray)
                    btn3.configure(bg = gray)
                    btn4.configure(bg = gray)
                    btn5.configure(bg = gray)

                    m=1

                    turn+=1
                    if turn<7:
                        trynum.config(text = str(turn)+'/6')
                    else: 
                        finishtext.configure(text = 'GAME OVER') # GAME FAIL (hopefully doesnt happen lol)
                        finishtext.place(x=700, y = 150)

                    
                    progress.config(value = (turn-1)/6*100)

                    colourer=1

                    #OUTPUT TO WORD LIST (MID LEFT)
                    all.insert('end', a[flags.index(3)])
                    
                    all.itemconfig(0, {'fg': green})
                    for n in range(0,12972):
                        if flags[n]==2:

                            all.insert('end', a[n])
                            all.itemconfig(colourer, {'fg': yellow})
                            colourer+=1
                        n+=1
                    for n in range(0,12972):
                        if flags[n]==0:
                            all.insert('end', a[n])
                        n+=1
                    flags[flags.index(3)]=2
                    



            #BACKSPACE INPUT

            elif key==Key.backspace:

                if m == 2:
                    try:
                        btn1.configure(text = '')
                        
                    except AttributeError:
                        print()
                    m-=1
                
                elif m == 3:
                    try:
                        btn2.configure(text = '')
                    except AttributeError:
                        print()
                    m-=1
                
                elif m == 4:
                    try:
                        btn3.configure(text = '')
                    except AttributeError:
                        print()
                    m-=1
                elif m == 5:
                    try:
                        btn4.configure(text = '')
                    except AttributeError:
                        print()

                    m-=1
                elif m == 6:
                    try:
                        btn5.configure(text = '')
                    except AttributeError:
                        print()

                    m-=1
            


            #LETTER INPUTS
            else:
                if m == 1:
                    try:
                        btn1.configure(text = '{0}'.format(key.char).upper())
                    except AttributeError:
                        print()
                    m+=1
                elif m == 2:
                    try:
                        btn2.configure(text = '{0}'.format(key.char).upper())
                    except AttributeError:
                        print()
                    m+=1
                
                elif m == 3:
                    try:
                        btn3.configure(text = '{0}'.format(key.char).upper())
                    except AttributeError:
                        print()
                    m+=1
                
                elif m == 4:
                    try:
                        btn4.configure(text = '{0}'.format(key.char).upper())
                    except AttributeError:
                        print()
                    m+=1
                elif m == 5:
                    try:
                        btn5.configure(text = '{0}'.format(key.char).upper())
                    except AttributeError:
                        print()
                    m+=1



def reset():
    #EVERY SINGLE VARIABLE AND CONDITION IS REVERTED
    global arr, flags, x, i, turn, m, all, prev, trynum, finish
    arr = [""]*50
    for ele in arr:
        ele = "!"
    i=1
    x = 0
    flags = [0]*12972
    turn = 1
    trynum.config(text = '1/6')
    progress.configure(value = 0)
    all.delete('0', 'end')
    prev.delete('0', 'end')

    btn1.configure(text = '')
    btn2.configure(text = '')
    btn3.configure(text = '')
    btn4.configure(text = '')
    btn5.configure(text = '')

    btn1.configure(bg = gray)
    btn2.configure(bg = gray)
    btn3.configure(bg = gray)
    btn4.configure(bg = gray)
    btn5.configure(bg = gray)

    finishtext.configure(text = '')
    finish = 0
    m=1





                        # LAYOUT SKELETON OF UI

#INPUT FIELDS
btn1 = tk.Button(root, text = ' ', width = 3, bg = gray,fg = 'white', activebackground = 'black', font = 'Verdana, 38', command = lambda: btncon(btn1))
btn1.place(x = 680 + 0*110, y = 480)

btn2 = tk.Button(root, text = ' ', width = 3, bg = gray,fg = 'white', activebackground = 'black', font = 'Verdana, 38', command = lambda: btncon(btn2))
btn2.place(x = 680 + 1*110, y = 480)

btn3 = tk.Button(root, text = ' ', width = 3, bg = gray, fg = 'white', activebackground = 'black', font = 'Verdana, 38', command = lambda: btncon(btn3))
btn3.place(x = 680 + 2*110, y = 480)

btn4 = tk.Button(root, text = ' ', width = 3, bg = gray, fg = 'white',activebackground = 'black', font = 'Verdana, 38', command = lambda: btncon(btn4))
btn4.place(x = 680 + 3*110, y = 480)

btn5 = tk.Button(root, text = ' ', width = 3, bg = gray, fg = 'white',activebackground = 'black', font = 'Verdana, 38', command = lambda: btncon(btn5))
btn5.place(x = 680 + 4*110, y = 480)





#QUIT BUTTON (TOP LEFT)
quit = tk.Button(root, text = 'QUIT', width = 5, bg = '#660000', activebackground='black', font = 'Impact, 38', command = exit)
quit.place(x=0,y=0)



#PROGRESS BAR(BOTTOM CENTRE)
progress = ttk.Progressbar(root, orient = 'horizontal', length = 640, mode = 'determinate')
progress.pack(side = 'bottom')
progress['value'] = 0
root.update_idletasks()


#WORD LIST (MID LEFT)
alltext = tk.Label(root, bg = backgroundcolor, fg = 'white', text = 'WORDS', font = 'Impact, 38')
alltext.place(x=383, y=200)


all = tk.Listbox(root, bg = gray, fg = 'white', height = 15, width = 15, selectbackground=green, selectforeground='black', selectborderwidth=0, highlightthickness=0, font = 'Impact, 20', justify = 'center')
all.place(x= 370, y = 280)


#WORD HISTORY (MID RIGHT)
prevtext = tk.Label(root, bg = backgroundcolor, fg = 'white', text = 'HISTORY', font = 'Impact, 38', justify='center')
prevtext.place(x=1300, y = 200)
prev = tk.Listbox(root, bg = gray, fg = 'white', height = 15, width = 15, font = 'Impact, 20')
prev.place(x= 1300, y = 280)


#GAME END TEXT (Revealed at end only)
finishtext = tk.Label(root, bg = backgroundcolor, fg = green, text = 'WORD FOUND', font = 'Impact, 60', justify='center')


#TRY COUNT
trytext = tk.Label(root, bg = backgroundcolor, fg = 'white', text = 'TRY', font = 'Impact, 38')
trytext.place(x=840,y=800)

trynum = tk.Label(root, bg = backgroundcolor, fg = 'white', text = '1/6', font = 'Impact, 38')
trynum.place(x=970, y = 800)


#RESET BUTTON (BOTTOM RIGHT)
resetbtn = tk.Button(root, text = 'RESET', width = 6, bg = yellow, activebackground='black', font = 'Impact, 30', command = reset)
resetbtn.place(x = 1760, y = 980)



                            # INITIALIZING UI AND LISTENERS

load_file_into_array()


listener =Listener(on_press = on_press, on_release = print(''))

mlistener = mouse.Listener(on_click = on_click)

mlistener.start()
listener.start()

root.mainloop()
listener.join()
mlistener.join()