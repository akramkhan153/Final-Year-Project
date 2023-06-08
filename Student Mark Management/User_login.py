from tkinter import *

from tkinter import messagebox,ttk,filedialog
import pymysql

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE),'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

user = Tk()
user.geometry('1920x1080+0+10')

bg = PhotoImage(file='pic1.png')
bgLabel = Label(user,image=bg)
bgLabel.place(x=0, y=0)

con = pymysql.connect(host="localhost",user="root",password="admin",database="studentregister")
cur = con.cursor()

def user_login():
    login_bg = '#FFF'
    global User_login_Frame
    User_login_Frame = Frame( padx=60, pady=60 , bg=login_bg )


    Label(User_login_Frame,text= 'User Login' , font= ('Arial',22,'bold') , bg=login_bg ).pack(pady=10)
    Label(User_login_Frame,text='Email',textvariable='email' , font= ('Arial',14), bg=login_bg ).pack(pady=1)
    entry01 = ttk.Entry(User_login_Frame)
    entry01.pack(pady=2)
    Label(User_login_Frame,text='Password', font= ('Arial',14) ,  bg=login_bg ).pack(pady=1)
    entry02 = ttk.Entry(User_login_Frame,show='*')
    entry02.pack(pady=2)

    def login_Close():
        if entry01.get() != '' and entry02.get() != '' :
            cur.execute("select * from userregister where Email=%s and Password=%s",(entry01.get(),entry02.get()))
            row = cur.fetchone()
            
            if row != None:
                if row[4] == 'Approved':
                    User_login_Frame.destroy()
                    search_Bar(row[1])
            

                else:
                    messagebox.showinfo('Wait','Wait For Admin Approval.')
            else:
                messagebox.showerror('Failed','Login Failed.')
        else:
            messagebox.showwarning("Alert","Enter Email & Password Correctly !!")

    def open_Register():
        User_login_Frame.destroy()
        user_Register()

    ttk.Button(User_login_Frame,text='Login ✔' ,command=login_Close).pack(pady=10)
    Button(User_login_Frame,text='Not Registered ?' , bd= 0 , bg=login_bg , relief='flat' , overrelief='flat' , command=open_Register ).pack(pady=10)
    User_login_Frame.pack()


import re

def user_Register():
    register_bg = '#FFF'
    register_Frame = Frame(padx=50, pady=20, bg=register_bg)
    Label(register_Frame, text='Register For User', font=('Arial', 22, 'bold'), bg=register_bg).pack(pady=10)

    # Validation function for email
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    # Validation function for name
    def validate_name(name):
        pattern = r'^[a-zA-Z ]+$'
        return re.match(pattern, name)

    # Validation function for password
    def validate_password(password):
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+=-]{8,}$'
        return re.match(pattern, password)

    Label(register_Frame, text='Name', underline=0, bg=register_bg).pack()
    reg_entry01 = ttk.Entry(register_Frame)
    reg_entry01.pack()
    Label(register_Frame, text='Email', bg=register_bg).pack()
    reg_entry02 = ttk.Entry(register_Frame)
    reg_entry02.pack()
    ttk.Label(register_Frame, text='Password', background=register_bg).pack()
    reg_entry03 = ttk.Entry(register_Frame, show='*')
    reg_entry03.pack()
    ttk.Label(register_Frame, text='Re-Enter Password', background=register_bg).pack()
    reg_entry04 = ttk.Entry(register_Frame, show='*')
    reg_entry04.pack()

    def register():
        name = reg_entry01.get().strip()
        email = reg_entry02.get().strip()
        password = reg_entry03.get().strip()

        if validate_name(name) and validate_email(email) and validate_password(password):
            cur.execute("SELECT Email, Name FROM userregister WHERE Email = %s OR Name = %s", (email, name))
            result = cur.fetchone()
            if result:
                if result[0] == email:
                    messagebox.showerror("Error", "Email already exists")
                else:
                    messagebox.showerror("Error", "Name already exists")
            elif reg_entry03.get() == reg_entry04.get():
                cur.execute("INSERT INTO userregister(Name, Email, Password, Status) VALUES(%s, %s, %s, 'Not Approved')", (name, email, password))
                con.commit()
                register_Frame.destroy()
                messagebox.showinfo('Success', 'Registered Successfully.')
                user_login()
            else:
                messagebox.showerror("Error", "Password and Re-Enter Password doesn't Match.")
        else:
            messagebox.showerror('Error', 'Enter a valid Name, Email and Password (password should be at least 8 characters long and contain only alphanumeric characters and special characters: !@#$%^&*()_+=-)')

    ttk.Button(register_Frame, text='Register', command=register).pack(pady=10)
    register_Frame.pack(pady=20)

user_login()




def search_Bar(name):
    user.title(f'Welcome {name} ')

    def search():
        cur.execute("SELECT o.`Sno`, o.`rollnum`, o.`owner_name`,  o.`name`, o.`status`, o.`file_key` FROM studentregister.studentreg o where Rollnum = %s ",(search_Entry.get()))
        result = cur.fetchall()
        
        admin = Tk()
        admin.title('User Search Results')
        admin_bg = '#FFF'
        admin_Frame = Frame( admin, padx=0, pady=20 , bg=admin_bg )

        if result:
            list = [ 'S.No', 'Rollnum', 'Owner Name' , 'User Name', 'Status ', 'File Key' ]
            for i in range(len(list)):
                en1 = ttk.Entry(admin_Frame)
                en1.grid(row=3,column=i)
                en1.insert(END, list[i])
                en1.config(state='disabled',foreground='darkblue',justify='center',font=('bold'),background='#000',)

            i=6
            b = {}
            for s in result:
                if s[len(s)-1] == 'Pending' :
                    for j in range(len(s)-1):
                        e = ttk.Entry(admin_Frame) 
                        e.grid(row=i,column=j)
                        e.insert(END, s[j])
                        e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))
                else:
                    for j in range(len(s)):
                        if j == len(s)-1:
                            e = ttk.Entry(admin_Frame) 
                            e.grid(row=i,column=j)
                            e.insert(END, s[j])
                            e.config(show='*',state='disabled',justify='center',foreground='#000',font=('Arial'))
                        elif s[j] == 'Verified':
                            b[s[j-1]] = ttk.Button(admin_Frame)
                            def approve( x= s[j-3] , y= s[j-2] ,z= s[len(s)-1] ):
                                cur.execute("insert into file_request(roll_num, owner_name, user_name,status,file_key) values(%s,%s,%s,'Requested',%s) ;",(x,y,name,z))
                                con.commit()
                                messagebox.showinfo('Succes','Done ✔')
                                admin.destroy()
                            b[s[j-1]].config(text= 'Request',command=approve)
                            b[s[j-1]].grid(row=i,column=j)

                        else:
                            e = ttk.Entry(admin_Frame) 
                            e.grid(row=i,column=j)
                            e.insert(END, s[j])
                            e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))


                i=i+1
        else :
            Label(admin_Frame,text='No Results Founded.').grid()

        admin_Frame.grid(row=5,column=10)
        admin.mainloop()

    def file_request(name):
        cur.execute("SELECT * FROM studentregister.file_request o where user_name = %s ",(name))
        result = cur.fetchall()
       
        admin = Tk()
        admin.title('User Search Results')
        admin_bg = '#FFF'
        admin_Frame = Frame( admin, padx=50, pady=20 , bg=admin_bg )

        if result:
            list = [ 'S.No', 'Roll Name','Owner Name', 'User Name' , 'Status ', 'File Key' ]
            for i in range(len(list)):
                en1 = ttk.Entry(admin_Frame,width=16)
                en1.grid(row=3,column=i)
                en1.insert(END, list[i])
                en1.config(state='disabled',foreground='darkblue',justify='center',font=('bold'),background='#000',)

            i=6
            b = {}
            for s in result:
                for j in range(len(s)):
                    if s[len(s)-2] == 'Accepted':  
                        e = ttk.Entry(admin_Frame,width=16) 
                        e.grid(row=i,column=j)
                        e.insert(END, s[j])
                        e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))

                            
                i+=1
            admin_Frame.pack()
            mainloop()

    def show_file():
        down_frame = Frame(background='#fff',padx=10,pady=10)
        ttk.Label(down_frame,text='Enter Your File Key').pack()
        l1 = Label(down_frame,background='#FFF')
        admin_bg = '#b3ffff'
        admin_Frame = Frame( down_frame, padx=10, pady=50 ,bg=admin_bg  )
                
        l1.pack()
        e1 = ttk.Entry()
        e1.pack()
        def submit():
           
                password = e1.get()
                def decrypt(enc, password):
                    private_key = hashlib.sha256(password.encode("utf-8")).digest()
                    enc = base64.urlsafe_b64decode(enc)
                    iv = enc[:16]
                    cipher = AES.new(private_key, AES.MODE_CBC, iv)
                    return unpad(cipher.decrypt(enc[16:]))
 

                
                cur.execute("SELECT * FROM studentregister.studentreg WHERE File_key = %s;",(e1.get()))
                result = cur.fetchall()
                if not result:
                    messagebox.showerror("ERROR",'key invalid')
                else:
                    
                    import tkinter as tk
                    
                    admin = tk.Tk()
                    admin.geometry('1250x700+0+10')
                   
                    admin_bg = '#69E2FF'
                    admin_Frame = Frame( admin, padx=10, pady=550 ,bg=admin_bg)
                    

                   
                    
                    list = ['S.no' ,'Rollnum', 'Name', 'Std', 'Subone', 'Subtwo', 'Subthree', 'Subfour', 'Subfive', 'Subsix', 'Total', 'Grade', 'Subseven', 'Subeight', 'Subnine', 'Subten', 'Subeleven', 'Subtwelve', 'Total1', 'Grade2', 'File_key', 'owner name']
                    for i in range(len(list)):
                        en1 = ttk.Entry(admin_Frame,width=7)
                        en1.grid(row=2,column=i)
                        en1.insert(END, list[i])
                       

                        
                    i=21 
                    b = {}
                   
                   
                    for s in result:
                        
                        for j in range(len(s)):
                            if s[j] == 'Verified':
                                b[s[j]] = ttk.Button(admin_Frame,width=16,)
                                
                                def approve(x1 = s[j-18], x2 = s[j-17], x3 = s[j-16], x4 = s[j-15], x5= s[j-14], x6 = s[j-13], x7 = s[j-12], x8 = s[j-11], x9 = s[j-10], x10 = s[j-9], x11 = s[j-8], x12 = s[j-7], x13 = s[j-6], x14 = s[j-5], x15 = s[j-4], x16 = s[j-3]):
                                    decrypted1 = decrypt(x1, password)
                                    decrypted2 = decrypt(x2, password)
                                    decrypted3 = decrypt(x3, password)
                                    decrypted4 = decrypt(x4, password)
                                    decrypted5 = decrypt(x5, password)
                                    decrypted6 = decrypt(x6, password)
                                    decrypted7 = decrypt(x7, password)
                                    decrypted8 = decrypt(x8, password)
                                    decrypted9 = decrypt(x9, password)
                                    decrypted10 = decrypt(x10, password)
                                    decrypted11 = decrypt(x11, password)
                                    decrypted12 = decrypt(x12, password)
                                    decrypted13 = decrypt(x13, password)
                                    decrypted14 = decrypt(x14, password)
                                    decrypted15 = decrypt(x15, password)
                                    decrypted16 = decrypt(x16, password)
                                   
                                  
                                    
                                  
                                   
                                   
                                 
                                    l2 = tk.Label(admin,text="SUB ONE:  "+ bytes.decode(decrypted1),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l2.place(x=200, y=100, width=300)
                                    l3 = tk.Label(admin,text="SUB TWO:  "+ bytes.decode(decrypted2),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l3.place(x=200, y=150, width=300)
                                    l4 = tk.Label(admin,text="SUB THREE:  "+ bytes.decode(decrypted3),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l4.place(x=200, y=200, width=300)
                                    l5 = tk.Label(admin,text="SUB FOUR:  "+ bytes.decode(decrypted4),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l5.place(x=200, y=250, width=300)

                                    l6 = tk.Label(admin,text="SUB FIVE:  "+ bytes.decode(decrypted5),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l6.place(x=200, y=300, width=300)

                                    l7 = tk.Label(admin,text="SUB SIX:  "+ bytes.decode(decrypted6),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l7.place(x=200, y=350, width=300)

                                    l8 = tk.Label(admin,text="TOTAL:  "+ bytes.decode(decrypted7),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l8.place(x=200, y=400, width=300)

                                    l9 = tk.Label(admin,text="GRADE:  "+ bytes.decode(decrypted8),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l9.place(x=200, y=450, width=300)

                                    l10 = tk.Label(admin,text="SUB ONE:  "+ bytes.decode(decrypted9),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l10.place(x=600, y=100, width=300)

                                    l11 = tk.Label(admin,text="SUB TWO:  "+ bytes.decode(decrypted10),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l11.place(x=600, y=150, width=300)

                                    l12 = tk.Label(admin,text="SUB THREE:  "+ bytes.decode(decrypted11),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l12.place(x=600, y=200, width=300)

                                    l13 = tk.Label(admin,text="SUB FOUR:  "+ bytes.decode(decrypted12),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l13.place(x=600, y=250, width=300)

                                    l14 = tk.Label(admin,text="SUB FIVE:  "+ bytes.decode(decrypted13),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l14.place(x=600, y=300, width=300)

                                    l15 = tk.Label(admin,text="SUB SIX:  "+ bytes.decode(decrypted14),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l15.place(x=600, y=350, width=300)

                                    l16 = tk.Label(admin,text="TOTAL:  "+ bytes.decode(decrypted15),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l16.place(x=600, y=400, width=300)

                                    l17 = tk.Label(admin,text="GRADE:  "+ bytes.decode(decrypted16),width=30,font=('Algerian', 16, 'bold'),bg='WHITE',
                                               fg='BLACK',)  
                                    l17.place(x=600, y=450, width=300)

                                    l18 =tk.Label(admin, text='FIRST SEMESTER', font=('times new roman', 18, 'bold'), bg='WHITE',
                                                fg='black', )
                                    l18.place(x=200, y=50, width=300)

                                    l19 =tk.Label(admin, text='SECOND SEMESTER', font=('times new roman', 16, 'bold'), bg='WHITE',
                                                fg='black', )
                                    l19.place(x=600, y=50, width=300)
                                    
                                    
                                    
                                    
                                b[s[j]].config(text= 'VIEW DATA',command=approve)
                            
                                b[s[j]].grid(row=i,column=j)
                                


                            else:
                                e = ttk.Entry(admin_Frame,width=5) 
                                e.grid(row=i,column=j)
                                e.insert(END, s[j])
                                e.config(state ='disabled',justify='center',foreground='#000',font=('Arial'))


                                     
                    i=i+1
                         
                    admin_Frame.grid(row=50,column=300)
                    admin.mainloop()
                   
    

                

        ttk.Button(down_frame,text='Submit',command=submit).pack()
        down_frame.pack()
        
    search_Frame = Frame(bg='#FFF',highlightcolor='#000',highlightbackground='#000',padx=10,pady=10,bd=1,)
    ttk.Label(search_Frame,text='Enter ROLL NUM ',font=('Bold'),background='#FFF').pack(pady=10)
    logout_Btn = ttk.Button(text='Logout' , command=user.destroy)
    logout_Btn.pack(padx=100,pady=10)
    search_Entry = ttk.Entry(search_Frame,width=100)
    search_Entry.pack(pady=10)
    ttk.Button(search_Frame,text='SEARCH',command=search).pack(pady=10)

    ttk.Button(search_Frame,text=' REQUESTED FILE',command=lambda : file_request(name)).pack()
    ttk.Button(search_Frame,text='SHOW FILE',command= show_file ).pack()

    search_Frame.pack()
def tab3():
    user.destroy()
    import main1
tab3_b=Button(user, text='HOME', font=('Times New Roman',13), command=tab3)
tab3_b.place(x=1300, y=20, height=30, width=130,)

mainloop()

