from tkinter import *
from tkinter import ttk
import pymysql
#from GIF import *

main = Tk()
main.geometry('1920x1080+0+10')
main.title("main")

main.config(bg = '#FFF') 

bg = PhotoImage(file='pic2.png')
bgLabel = Label(main, image=bg)
bgLabel.place(x=0, y=0)
                

main_Frame = Frame(main ,pady=10)
m_x = 10

def tab6():
    main.destroy()
    import main1


def tab1():
    main.destroy()
    import Staff_login

def tab2():
    main.destroy()
    import admin
def tab3():
    main.destroy()
    import main1
def tab4():
    main.destroy()
    import User_login
def tab5():
    main.destroy()
    import main1
    
    

tab3_b=Button(main, text='HOME', font=('Times New Roman',20), command=tab3)
tab3_b.place(x=750, y=100, height=40, width=150,)

tab4_b=Button(main, text='TEACHER LOGIN', font=('Times New Roman',13), command=tab1)
tab4_b.place(x=750, y=200, height=40, width=150,)

tab1_b=Button(main, text='USER LOGIN', font=('Times New Roman',15), command=tab4)
tab1_b.place(x=750, y=300, height=40, width=150,)

tab2_b=Button(main, text='ADMIN', font=('Times New Roman',15), command=tab2)
tab2_b.place(x=750, y=400, height=40, width=150,)    



mainloop()

