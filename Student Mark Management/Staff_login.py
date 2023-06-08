from tkinter import *
import re
from tkinter import messagebox,ttk,filedialog
import pymysql,os
from pymysql import connect, err, sys, cursors
from random import *
from cryptography.fernet import Fernet
con = pymysql.connect(host="localhost",user="root",password="admin",database="studentregister")
cur = con.cursor()

root= Tk()
root.geometry('1920x1080+0+10')

bg = PhotoImage(file='pic1.png')
bgLabel = Label(root,image=bg)
bgLabel.place(x=0, y=0)
 
def owner_login():

   login_bg = '#FFF'
   global login_Frame
   login_Frame = Frame( padx=50, pady=20 , bg=login_bg )
   Label(login_Frame,text= 'Teacher Login' , font= ('Arial',22,'bold') , bg=login_bg ).pack(pady=10)
   Label(login_Frame,text='Email',textvariable='email' , font= ('Arial',14), bg=login_bg ).pack(pady=1)
   entry01 = ttk.Entry(login_Frame)
   entry01.pack(pady=2)
   Label(login_Frame,text='Password' , font= ('Arial',14),  bg=login_bg ).pack(pady=1)
   entry02 = ttk.Entry(login_Frame,show='*')
   entry02.pack(pady=2)

   def login_Close():
      if entry01.get() != '' and entry02.get() != '':
            cur.execute("select * from registerloginform where Email=%s and Password=%s",(entry01.get(),entry02.get()))
            row = cur.fetchone()
            #print(row)
            if row != None:
                if row[4] == 'Approved':
                    login_Frame.destroy()
                    staff_screen(row[1])
                    
                else:
                    messagebox.showinfo('Wait','Wait For Admin Approval.')
            else:
                messagebox.showerror('Failed','Login Failed.')
      else:
         messagebox.showwarning("Alert","Enter Email & Password Correctly !!")
   def tab3():
    root.destroy()
    import main1
   tab3_b=Button(root, text='HOME', font=('Times New Roman',13), command=tab3)
   tab3_b.place(x=1200, y=10, height=30, width=130,)


  
   def open_Register():
        login_Frame.destroy()
        owner_Register()

   ttk.Button(login_Frame,text='Login ✔' ,command=login_Close).pack(pady=10)
   Button(login_Frame,text='Not Registered ?' , bd= 0 , bg=login_bg , relief='flat' , overrelief='flat' , command=open_Register ).pack(pady=10)
   login_Frame.pack()
      

def owner_Register():
    register_bg = '#FFF'
    register_Frame = Frame(padx=50, pady=20, bg=register_bg)
    Label(register_Frame, text='Teacher Register', font=('Arial', 22, 'bold'), bg=register_bg).pack(pady=10)

    Label(register_Frame, text='Name', underline=0, bg=register_bg).pack()
    reg_entry01 = ttk.Entry(register_Frame)
    reg_entry01.pack()

    Label(register_Frame, text='Email', bg=register_bg).pack()
    reg_entry02 = ttk.Entry(register_Frame)
    reg_entry02.pack()

    Label(register_Frame, text='Password', background=register_bg).pack()
    reg_entry03 = ttk.Entry(register_Frame, show='*')
    reg_entry03.pack()

    show_password = BooleanVar()

    def toggle_show_password():
        if show_password.get():
            reg_entry03.configure(show='')
        else:
            reg_entry03.configure(show='*')

    ttk.Checkbutton(register_Frame, text='Show Password', variable=show_password, command=toggle_show_password,
                     onvalue=True, offvalue=False).pack()

    Label(register_Frame, text='Re-Enter Password', background=register_bg).pack()
    reg_entry04 = ttk.Entry(register_Frame, show='*')
    reg_entry04.pack()

    def register():
        name = reg_entry01.get()
        email = reg_entry02.get()
        password = reg_entry03.get()
        confirm_password = reg_entry04.get()

        # Check for valid name
        if not name or not re.match(r'^[a-zA-Z ]+$', name):
            messagebox.showerror('Error', 'Enter a valid name')
            return

        # Check for valid email
        if not email or not re.match(r'^\S+@\S+\.\S+$', email):
            messagebox.showerror('Error', 'Enter a valid email')
            return

        # Check for valid password
        if not password or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            messagebox.showerror('Error', 'Password should be at least 8 characters long and contain both letters and numbers')
            return

        # Check for matching passwords
        if password != confirm_password:
            messagebox.showerror("Error", "Password and Re-Enter Password doesn\'t Match.")
            return

        # Check if the name  are already registered
        cur.execute("SELECT * FROM registerloginform WHERE Name=%s ", (name))
        result = cur.fetchone()
        if result:
            messagebox.showerror("Error", "This name  is already registered.")
            return

        # Check if the  email are already registered
        cur.execute("SELECT * FROM registerloginform WHERE  Email=%s", (email))
        result = cur.fetchone()
        if result:
            messagebox.showerror("Error", "This email is already registered.")
            return

        # Add the user to the database
        cur.execute("INSERT INTO registerloginform (Name, Email, Password, Status) VALUES (%s, %s, %s, 'Not Approved')", (name, email, password))
        con.commit()

        messagebox.showinfo('Success', 'Registration successful.')
        register_Frame.destroy()
        owner_login()
    logout_Btn = ttk.Button(text='Logout' , command=root.destroy)
    ttk.Button(register_Frame, text='Register', command=register).pack(pady=10)
    register_Frame.pack(pady=20)

owner_login()



def file_request(name):
    
    cur.execute("SELECT * FROM studentregister.file_request WHERE Owner_name = %s ;",(name))
    result = cur.fetchall()
   # print(*result)
    admin = Tk()
   

    admin_bg = '#FFF'
    admin_Frame = Frame( admin, padx=0, pady=20 , bg=admin_bg )
    
    list = [ 'S.No' , 'Roll_Num' , 'Owner_Name' , 'User_Name' , 'Status ' , 'File_Key' ]
    for i in range(len(list)):
        en1 = ttk.Entry(admin_Frame,width=16)
        en1.grid(row=3,column=i)
        en1.insert(END, list[i])
        en1.config(state='disabled',foreground='darkblue',justify='center',font=('bold'),background='#000',)

    i=6
    b = {}
    for s in result:
        for j in range(len(s)):
            if s[j] == 'Requested':
                b[s[j]] = ttk.Button(admin_Frame,width=16)
                def approve( x = s[j+1] ):
                    cur.execute("UPDATE file_request SET status = 'Accepted' WHERE file_key = %s;",(x))
                    con.commit()
                    #print(x)
                    messagebox.showinfo('Success','Done ✔')
                    admin.destroy()
                b[s[j]].config(text= 'Accept Request',command=approve)
                b[s[j]].grid(row=i,column=j)
            else:
                e = ttk.Entry(admin_Frame,width=16) 
                e.grid(row=i,column=j)
                e.insert(END, s[j])
                e.config(state ='disabled',justify='center',foreground='#000',font=('Arial'))

   
    admin_Frame.grid(row=5,column=10)
    
    admin.mainloop()
    
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
 
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE),'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]




    
def staff_screen(name):
    def fileupload():
          
       
           root.title(f'{name}')
           l1 = ttk.Label()
           l1.pack()

           key = [chr(x) for x in range(65,91) ]
           keys = ''
       
           for i in range(6):
                 keys += choice(key)
       
           Key_Label = ttk.Label(text=f'Key : {keys}')
           Key_Label.pack()
           titleLabel = Label(text='STUDENT DETAILS', font=('Times New Roman', 22, 'bold '), bg='white',
                              fg='black', )
           titleLabel.place(x=390, y=70)

           rollnumLabel = Label( text='ROLL ', font=('times new roman', 18, 'bold'), bg='white',
                          fg='black', )
           rollnumLabel.place(x=15, y=140, width=150)
           entryRollnum = Entry( font=('times new roman', 18), bg='lightgray')
           entryRollnum.place(x=180, y=140, width=150)

           nameLabel = Label(text=' NAME', font=('times new roman', 18, 'bold'), bg='white',
                             fg='black', )
           nameLabel.place(x=360, y=140, width=150)
           entryName= Entry(font=('times new roman', 18), bg='lightgray')
           entryName.place(x=530, y=140, width=150)

           StdLabel = Label( text='DEPARTMENT', font=('times new roman', 15, 'bold'), bg='white',
                        fg='black', )
           StdLabel.place(x=700, y=140, width=150)
           entryStd = Entry( font=('times new roman', 18), bg='lightgray')
           entryStd.place(x=860, y=140, width=150)

           semesterLabel = Label( text='FIRST SEMESTER', font=('times new roman', 15, 'bold'), bg='white',
                         fg='black', )
           semesterLabel.place(x=150, y=200, width=200)

           modelexamLabel = Label( text='SECOND SEMESTER', font=('times new roman', 15, 'bold'), bg='white',
                         fg='black', )
           modelexamLabel.place(x=590, y=200, width=200)
           sub1Label = Label( text='SUB1', font=('times new roman', 18, 'bold'), bg='white', fg='black', )
           sub1Label.place(x=15, y=260, width=150)
           Subone = Entry( font=('times new roman', 18), bg='lightgray')
           Subone.place(x=250, y=260, width=150)
           sub2Label = Label( text='SUB2', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub2Label.place(x=15, y=300, width=150)
           Subtwo= Entry(font=('times new roman', 18), bg='lightgray',)
           Subtwo.place(x=250, y=300, width=150)
           sub3Label = Label( text='SUB3', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           sub3Label.place(x=15, y=340, width=150)
           Subthree = Entry( font=('times new roman', 18), bg='lightgray')
           Subthree.place(x=250, y=340, width=150)

           sub4Label = Label( text='SUB4', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub4Label.place(x=15, y=380, width=150)
           Subfour = Entry(font=('times new roman', 18), bg='lightgray',)
           Subfour.place(x=250, y=380, width=150)
           sub5Label = Label(text='SUB5', font=('times new roman', 18, 'bold'), bg='white',
                             fg='black', )
           sub5Label.place(x=15, y=420, width=150)
           Subfive = Entry(font=('times new roman', 18), bg='lightgray')
           Subfive.place(x=250, y=420, width=150)
           sub6Label = Label( text='SUB6', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub6Label.place(x=15, y=460, width=150)
           Subsix = Entry(font=('times new roman', 18), bg='lightgray',)
           Subsix.place(x=250, y=460, width=150)


          

           sub1Label = Label( text='SUB1', font=('times new roman', 18, 'bold'), bg='white', fg='black', )
           sub1Label.place(x=500, y=260, width=150)
           Subseven = Entry( font=('times new roman', 18), bg='lightgray')
           Subseven.place(x=700, y=260, width=150)
           sub2Label = Label( text='SUB2', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub2Label.place(x=500, y=300, width=150)
           Subeight = Entry(font=('times new roman', 18), bg='lightgray',)
           Subeight.place(x=700, y=300, width=150)
           sub3Label = Label(text='SUB3', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           sub3Label.place(x=500, y=340, width=150)
           Subnine= Entry( font=('times new roman', 18), bg='lightgray')
           Subnine.place(x=700, y=340, width=150)

           sub4Label = Label(text='SUB4', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub4Label.place(x=500, y=380, width=150)
           Subten = Entry(font=('times new roman', 18), bg='lightgray',)
           Subten.place(x=700, y=380, width=150)


           sub5Label = Label( text='SUB5', font=('times new roman', 18, 'bold'), bg='white',
                         fg='black', )
           sub5Label.place(x=500, y=420, width=150)
           Subeleven = Entry( font=('times new roman', 18), bg='lightgray')
           Subeleven.place(x=700, y=420, width=150)

           sub6Label = Label( text='SUB6', font=('times new roman', 18, 'bold'), bg='white',
                       fg='black', )
           sub6Label.place(x=500, y=460, width=150)
           Subtwelve = Entry(font=('times new roman', 18), bg='lightgray',)
           Subtwelve.place(x=700, y=460, width=150)
          
           


           check = IntVar() 
           def upload():
               if entryRollnum.get() == '' or entryName.get() == '' or entryStd.get() == '' or Subone.get()== '' or \
                   Subtwo.get() == '' or Subthree.get() == '' or Subfour.get() == '' or Subfive.get()== '' or \
                   Subsix.get() == ''   or Subseven.get()== '' or \
                   Subeight.get() == '' or Subnine.get() == '' or Subten.get() == '' or Subeleven.get()== '' or \
                       Subtwelve.get() == '':
                       messagebox.showerror('Error', "All Fields Are Required")
       
       

               else:
                   try:
                       password = keys

                       def calculate_grade(total_marks):
                            if total_marks >= 80:
                                return 4.00
                            elif total_marks >= 75:
                                return 3.75
                            elif total_marks >= 70:
                                return 3.50
                            elif total_marks >= 65:
                                return 3.25
                            elif total_marks >= 60:
                                return 3.00
                            elif total_marks >= 55:
                                return 2.75
                            elif total_marks >= 50:
                                return 2.50
                            elif total_marks >= 45:
                                return 2.25
                            elif total_marks >= 40:
                                return 2.00
                            else:
                                return 0
    
                       def encrypt(raw, password):
                           private_key = hashlib.sha256(password.encode("utf-8")).digest()
                           raw = pad(raw)
                           iv = Random.new().read(AES.block_size)
                           cipher = AES.new(private_key, AES.MODE_CBC, iv)
                           return base64.urlsafe_b64encode(iv + cipher.encrypt(raw))
                        
                       message1 = int(Subone.get())
                       message01 = calculate_grade(message1)
                       message2 = int(Subtwo.get())
                       message02 = calculate_grade(message2)
                       message3 = int(Subthree.get())
                       message03 = calculate_grade(message3)
                       message4 = int(Subfour.get())
                       message04 = calculate_grade(message4)
                       message5 = int(Subfive.get())
                       message05 = calculate_grade(message5)
                       message6 = int(Subsix.get())
                       message06 = calculate_grade(message6)
                       message7 = message1 + message2 + message3 + message4 + message5 + message6
                       message07 = message01 +message02 + message03 + message04 + message05 + message06
                       message0001= message07/ 6.0
                       message8 = "{:.2f}".format(message0001)
                       message9 = int(Subseven.get())
                       message09 = calculate_grade(message9)
                       message10 = int(Subeight.get())
                       message010 = calculate_grade(message10)
                       message11 = int(Subnine.get())
                       message011 = calculate_grade(message11)
                       message12 = int(Subten.get())
                       message012 = calculate_grade(message12)
                       message13 = int(Subeleven.get())
                       message013 = calculate_grade(message13)
                       message14 = int(Subtwelve.get())
                       message014 = calculate_grade(message14)
                       message15 = message9 + message10 + message11 + message12 + message13 + message14
                       message015 = message09 + message010 + message011 + message012 + message013 + message014
                       message0011= message015/ 6.0
                       message16 = "{:.2f}".format(message0011)
                       encrypted1 = encrypt( str(message1), password)
                       encrypted2 = encrypt( str(message2), password)
                       encrypted3 = encrypt( str(message3), password)
                       encrypted4 = encrypt( str(message4), password)
                       encrypted5 = encrypt( str(message5), password)
                       encrypted6 = encrypt( str(message6), password)
                       encrypted7 = encrypt( str(message7), password)
                       encrypted8 = encrypt( str(message8), password)
                       encrypted9 = encrypt( str(message9), password)
                       encrypted10 = encrypt( str(message10), password)
                       encrypted11 = encrypt( str(message11), password)
                       encrypted12 = encrypt( str(message12), password)
                       encrypted13 = encrypt( str(message13), password)
                       encrypted14 = encrypt( str(message14), password)
                       encrypted15 = encrypt( str(message15), password)
                       encrypted16 = encrypt( str(message16), password)
                       con = pymysql.connect(host='localhost', user='root', password='admin', database='studentregister')
                       cur = con.cursor()
                       cur.execute("insert into studentreg (Rollnum, Name, Std, Subone, Subtwo, Subthree, Subfour, Subfive, Subsix, Total, Grade, Subseven, Subeight, Subnine, Subten, Subeleven, Subtwelve, Total1, Grade2, File_key, Owner_name, Status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')", (entryRollnum.get(), entryName.get(), entryStd.get(), encrypted1, encrypted2, encrypted3, encrypted4, encrypted5, encrypted6, encrypted7,encrypted8, encrypted9, encrypted10, encrypted11, encrypted12, encrypted13, encrypted14, encrypted15, encrypted16, password,name))
                       con.commit()
                       con.close()
                       messagebox.showinfo('Success', "Registration Successful")
                   except Exception as e:
                       showerror('Error', f"Error due to: {e}",)
                          
           registerbutton = Button(text="SUBMIT", bd=4, bg='white', command=upload, activebackground='white', activeforeground='white',)
           registerbutton.place(x=300, y=620, width=100, height=40)
           clearbutton = Button( text="CLEAR", bd=4, bg='white', command=fileupload, activebackground='white', activeforeground='white',)
           clearbutton.place(x=500, y=620, width=100, height=40)
           
             
           
                
    upload_Btn = ttk.Button(text='register',command=fileupload )        
    upload_Btn.pack()
    
    file_request(name)

 
    
#logout_Btn = ttk.Button(text='Logout' , command=root.destroy)
logout_Btn.pack(padx=100,pady=10)
mainloop()


