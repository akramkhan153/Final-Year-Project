from tkinter import *
from tkinter import messagebox,ttk
import pymysql
import smtplib
root= Tk()
root.geometry('1920x1080+0+10')
bg = PhotoImage(file='pic3.png')
bgLabel = Label(root,image=bg)
bgLabel.place(x=0, y=0)
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE),'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def user_register():
    con = pymysql.connect(host="localhost",user="root",password="admin",database="studentregister")
    cur = con.cursor()
    cur.execute("SELECT * FROM studentregister.userregister ;") 
    result = cur.fetchall()
    
    admin = Tk()
    
    admin.title('User Register')
    admin_bg = '#FFF'
    admin_Frame = Frame( admin, padx=50, pady=20 , bg=admin_bg )
   
   

    list = [ 'S.No', 'Name', 'Email' , 'Password' , 'Status ' ]
    for i in range(len(list)):
        en1 = ttk.Entry(admin_Frame)
        en1.grid(row=3,column=i)
        en1.insert(END, list[i])
        en1.config(state='disabled',foreground='darkblue',justify='center',font=('bold'),background='#000',)

    i=6
    b = {}
    for s in result:
        if s[len(s)-1] == 'Approved' :
            for j in range(len(s)):
                e = ttk.Entry(admin_Frame) 
                e.grid(row=i,column=j)
                e.insert(END, s[j])
                e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))
        else:
            for j in range(len(s)):
                if s[j] == 'Not Approved':
                    print(s[j],'->',s[j-2])
                    b[s[j-2]] = ttk.Button(admin_Frame)
                    def approve(x=s[j-2] ):
                        cur.execute("UPDATE userregister SET Status = 'Approved' WHERE Email = %s;",(x))
                        con.commit()
                        messagebox.showinfo('Succes','Done ✔')
                        admin.destroy()
                    b[s[j-2]].config(text= 'Approve',command=approve)
                    b[s[j-2]].grid(row=i,column=j)
                else:
                    e = ttk.Entry(admin_Frame) 
                    e.grid(row=i,column=j)
                    e.insert(END, s[j])
                    e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))

        i=i+1

    admin_Frame.grid(row=5,column=10)
    admin.mainloop()

def owner_register():
    con = pymysql.connect(host="localhost",user="root",password="admin",database="studentregister")
    cur = con.cursor()
    cur.execute("SELECT * FROM studentregister.registerloginform ;") 
    result = cur.fetchall()
    
    admin = Tk()
    
    admin.title('Staff Register')
    admin_bg = '#FFF'
    admin_Frame = Frame( admin, padx=50, pady=20 , bg=admin_bg )

    list = [ 'S.No', 'Name', 'Email' , 'Password' , 'Status ' ]
    for i in range(len(list)):
        en1 = ttk.Entry(admin_Frame)
        en1.grid(row=3,column=i)
        en1.insert(END, list[i])
        en1.config(state='disabled',foreground='darkblue',justify='center',font=('bold'),background='#000',)

    i=6
    b = {}
    for s in result:
        if s[len(s)-1] == 'Approved' :
            for j in range(len(s)):
                e = ttk.Entry(admin_Frame) 
                e.grid(row=i,column=j)
                e.insert(END, s[j])
                e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))
        else:
            for j in range(len(s)):
                if s[j] == 'Not Approved':
                    b[s[j-2]] = ttk.Button(admin_Frame)
                    def approve(x = s[j-2]):
                        cur.execute("UPDATE registerloginform SET Status = 'Approved' WHERE Email = %s;",(x))
                        con.commit()
                        messagebox.showinfo('Succes','Done ✔')
                        admin.destroy()
                    b[s[j-2]].config(text= 'Approve',command=approve)
                    b[s[j-2]].grid(row=i,column=j)
                else:
                    e = ttk.Entry(admin_Frame) 
                    e.grid(row=i,column=j)
                    e.insert(END, s[j])
                    e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))

        i=i+1

    admin_Frame.grid(row=5,column=10)
    admin.mainloop()

def owner_verify():
    con = pymysql.connect(host="localhost",user="root",password="admin",database="studentregister")
    cur = con.cursor()
    cur.execute("SELECT Sno, Rollnum, Name, Std, File_Key, Owner_name, Status  FROM studentregister.studentreg ;")
    result = cur.fetchall()
   
    admin = Tk()
   
    admin.title('Verify Files')
    admin.geometry('1200x600+0+10')
    admin_bg = '#FFF'
    
    admin_Frame = Frame( admin, padx=0, pady=50 , bg=admin_bg )

    list = ['Sno','Rollnum' , 'Name', 'Std' , 'File_Key ','Owner Name','Status']
    for i in range(len(list)):
        en1 = ttk.Entry(admin_Frame,width=8)
        en1.grid(row=3,column=i)
        en1.insert(END, list[i])
        en1.config(state='disabled',foreground ='darkblue',justify='center',font=('bold'),background='#000',)

    i=8
    b = {}
    for s in result:
        if s[len(s)-1] == 'Verified' :
            for j in range(len(s)):
                e = ttk.Entry(admin_Frame,width=8) 
                e.grid(row=i,column=j)
                e.insert(END, s[j])
                e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))
        else:
            for j in range(len(s)):
                if s[j] == 'Pending':
                    b[s[j-2]] = ttk.Button(admin_Frame,width=10)
                    def approve( x = [s[j-2]] ):
                        
                        cur.execute("UPDATE studentreg SET status = 'Verified' WHERE file_key = %s;",(x))
                        con.commit()
                        messagebox.showinfo('Success','Done ✔')
                        admin.destroy()
                        
                    b[s[j-2]].config(text= 'Verify',command=approve)
                    b[s[j-2]].grid(row=i,column=j)
                else:
                    e = ttk.Entry(admin_Frame,width=8) 
                    e.grid(row=i,column=j)
                    e.insert(END, s[j])
                    e.config(state='disabled',justify='center',foreground='#000',font=('Arial'))

        i=i+1
        
        e1 = ttk.Entry(admin_Frame,width=10)
        e1.grid(row=1,column=1)
        
        def view():
            
           
                    password = e1.get()
                    def decrypt(enc, password):
                        private_key = hashlib.sha256(password.encode("utf-8")).digest()
                        enc = base64.urlsafe_b64decode(enc)
                        iv = enc[:16]
                        cipher = AES.new(private_key, AES.MODE_CBC, iv)
                        return unpad(cipher.decrypt(enc[16:]))
                
 

                
                    cur.execute("SELECT * FROM studentregister.studentreg WHERE File_key = %s;",(e1.get()))
                    result = cur.fetchall()
                    
                    i=21 
                    b = {}
                       
                       
                    for s in result:
                        #for j in range(len(s)):
                            #if s[j] == 'Verified':
                                #b[s[j]] =Button(width=16,)
                                

                                def approve(x1 = s[j-1], x2 = s[j-2], x3 = s[j-0], x4 = s[j+1], x5= s[j+2], x6 = s[j-13], x7 = s[j-12], x8 = s[j-11], x9 = s[j-10], x10 = s[j+9], x11 = s[j+8], x12 = s[j+7], x13 = s[j+6], x14 = s[j+5], x15 = s[j+4], x16 = s[j+3]):
                                    
                                    decrypted1 = decrypt(x1, password)
                                    print(decrypted1)
                                    decrypted2 = decrypt(x2, password)
                                    print(decrypted2)
                                    decrypted3 = decrypt(x3, password)
                                    print(decrypted3)
                                    decrypted4 = decrypt(x4, password)
                                    print(decrypted4)
                                    decrypted5 = decrypt(x5, password)
                                    print(decrypted5)
                                    decrypted6 = decrypt(x6, password)
                                    print(decrypted6)
                                    decrypted7 = decrypt(x7, password)
                                    print(decrypted7)
                                    decrypted8 = decrypt(x8, password)
                                    print(decrypted8)
                                    decrypted9 = decrypt(x9, password)
                                    print(decrypted9)
                                    decrypted10 = decrypt(x10, password)
                                    print(decrypted10)
                                    decrypted11 = decrypt(x11, password)
                                    print(decrypted11)
                                    decrypted12 = decrypt(x12, password)
                                    print(decrypted12)
                                    decrypted13 = decrypt(x13, password)
                                    print(decrypted13)
                                    decrypted14 = decrypt(x14, password)
                                    print(decrypted14)
                                    decrypted15 = decrypt(x15, password)
                                    print(decrypted15)
                                    decrypted16 = decrypt(x16, password)
                                    print(decrypted16)
                                    
                                    l2 = ttk.Label(admin,text="SUB ONE:  "+ bytes.decode(decrypted2),width=30,font=('Algerian', 16, 'bold'))
                                    l2.place(x=700, y=100, width=300)
                                    l3 = ttk.Label(admin,text="SUB TWO:  "+ bytes.decode(decrypted1),width=30,font=('Algerian', 16, 'bold'))
                                                     
                                    l3.place(x=700, y=150, width=300)
                                    l4 = ttk.Label(admin,text="SUB THREE:  "+ bytes.decode(decrypted3),width=30,font=('Algerian', 16, 'bold'))
                                                     
                                    l4.place(x=700, y=200, width=300)
                                    l5 = ttk.Label(admin,text="SUB FOUR:  "+ bytes.decode(decrypted4),width=30,font=('Algerian', 16, 'bold'))
                                                  
                                    l5.place(x=700, y=250, width=300)

                                    l6 = ttk.Label(admin,text="SUB FIVE:  "+ bytes.decode(decrypted5),width=30,font=('Algerian', 16, 'bold'))
                                                 
                                    l6.place(x=700, y=300, width=300)

                                    l7 = ttk.Label(admin,text="SUB SIX:  "+ bytes.decode(decrypted16),width=30,font=('Algerian', 16, 'bold'))
                                                    
                                    l7.place(x=700, y=350, width=300)

                                    l8 = ttk.Label(admin,text="TOTAL:  "+ bytes.decode(decrypted15),width=30,font=('Algerian', 16, 'bold'))                                                   
                                    l8.place(x=700, y=400, width=300)

                                    l9 = ttk.Label(admin,text="GRADE:  "+ bytes.decode(decrypted14),width=30,font=('Algerian', 16, 'bold'))
                                                   
                                    l9.place(x=700, y=450, width=300)

                                    l10 = ttk.Label(admin,text="SUB ONE:  "+ bytes.decode(decrypted13),width=30,font=('Algerian', 16, 'bold'))
                                                     
                                    l10.place(x=950, y=100, width=300)

                                    l11 = ttk.Label(admin,text="SUB TWO:  "+ bytes.decode(decrypted12),width=30,font=('Algerian', 16, 'bold'))
                                                   
                                    l11.place(x=950, y=150, width=300)

                                    l12 = ttk.Label(admin,text="SUB THREE:  "+ bytes.decode(decrypted11),width=30,font=('Algerian', 16, 'bold'))
                                                   
                                    l12.place(x=950, y=200, width=300)

                                    l13 = ttk.Label(admin,text="SUB FOUR:  "+ bytes.decode(decrypted10),width=30,font=('Algerian', 16, 'bold'))                                                   
                                    l13.place(x=950, y=250, width=300)

                                    l14 = ttk.Label(admin,text="SUB FIVE:  "+ bytes.decode(decrypted6),width=30,font=('Algerian', 16, 'bold'))
                                                  
                                    l14.place(x=950, y=300, width=300)

                                    l15 = ttk.Label(admin,text="SUB SIX:  "+ bytes.decode(decrypted7),width=30,font=('Algerian', 16, 'bold'))
                                                   
                                    l15.place(x=950, y=350, width=300)

                                    l16 = ttk.Label(admin,text="TOTAL:  "+ bytes.decode(decrypted8),width=30,font=('Algerian', 16, 'bold'))
                                                    
                                    l16.place(x=950, y=400, width=300)

                                    l17 = ttk.Label(admin,text="GRADE:  "+ bytes.decode(decrypted9),width=30,font=('Algerian', 16, 'bold'))
                                                   
                                    l17.place(x=950, y=450, width=300)

                                    l18 =ttk.Label(admin, text=' SEMESTER', font=('times new roman', 18, 'bold')) 
                                                    
                                    l18.place(x=700, y=50, width=250)

                                    l19 =ttk.Label(admin, text=' MODEL EXAM', font=('times new roman', 18, 'bold')) 
                                                    
                                    l19.place(x=950, y=50, width=250)
                                        
                                        
                                        
                                l2=ttk.Button(admin_Frame,text= 'ENTER',command = approve,width=10)
                                l2.grid(row=1,column =2)        
                                
            
                                
                        
                                

                                     
                    i=i+1
            
        l1=ttk.Button(admin_Frame,text= 'CLICK',command = view,width=10)
        l1.grid(row=1,column =0)
        

    admin_Frame.grid(row=10,column=80)
    admin.mainloop()
   
logout_Btn = ttk.Button(text='Logout' , command=root.destroy)
logout_Btn.pack(padx=100,pady=10)
 

img_user = PhotoImage(file = "Assets/user1.png").subsample(3,3)
ttk.Button(text='USER DETAILS' , image= img_user, compound=TOP  ,command=user_register).pack()
img_owner = PhotoImage(file = "Assets/Owner.png").subsample(1,1)
ttk.Button(text='TEACHER DETAILS' , image=img_owner , compound=TOP ,command=owner_register).pack()
img_verify = PhotoImage(file = "Assets/verified.png").subsample(8,8)
ttk.Button(text='VERIFY TEACHER FILE' , image=img_verify , compound=TOP ,command=owner_verify ).pack()
def tab3():
    user.destroy()
    import main1
tab3_b=Button(user, text='HOME', font=('Times New Roman',13), command=tab3)
tab3_b.place(x=1300, y=20, height=30, width=130)
mainloop()
