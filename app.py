import re
import os
import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext, messagebox, filedialog
import main
import sqlite3

app_list = []
attach_list = []


def add_db(email, password, listBox):
    global app_list
    if (re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", str(email)) and password != ""):
        conn = sqlite3.connect('emails.db')
        c = conn.cursor()
        c.execute(r"INSERT INTO emails VALUES(:email, :pass)",
                  {
                      'email': email,
                      'pass': password
                  })
        conn.commit()
        conn.close()
        app_list.append([email, password])
        for child in listBox.get_children():
            listBox.delete(child)
        for i in (app_list):
            listBox.insert(parent='', index='end',
                           values=(i[0], (len(i[1])*"*")))
        email_vals.append(email)
    else:
        messagebox.showerror(
            "Error", "Either the Email is wrong or the Password is blank")


def toggle_password(passwd_entry, toggle_btn):
    if passwd_entry.cget('show') == '':
        passwd_entry.config(show='*')
        toggle_btn.config(text='Show')
    else:
        passwd_entry.config(show='')
        toggle_btn.config(text='Hide')


def add_to_list():
    global app_list
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute("SELECT * FROM emails")
    rec = c.fetchall()
    for r in rec:
        app_list.append([r[0], r[1]])
    conn.commit()
    conn.close()


def add(listBox):
    global app_list
    add_email = tk.Toplevel()
    add_email.title("Add Email")
    add_email.geometry("400x340")
    if ("nt" == os.name):
        add_email.iconbitmap("./icon.ico")
    add_email.resizable(0, 0)
    canvas = tk.Canvas(add_email, width=400, height=340, bg="#070769")
    canvas.pack(fill=tk.BOTH)
    canvas.create_text(200, 30, fill="white", font="Arial 20 bold",
                       text="Add Mail")
    canvas.create_text(66, 90, fill="white",
                       font="Arial 12", text="Email Address")
    email = tk.Entry(add_email, width=30, font="Arial 16",
                     relief="groove", borderwidth=0)
    email.place(x=16, y=110)
    canvas.create_text(52, 170, fill="white",
                       font="Arial 12", text="Password")
    password = tk.Entry(add_email, show="*", width=22,
                        font="Arial 16", relief="groove", borderwidth=0)
    toggle_btn = tk.Button(add_email, text='Show', width=12,
                           command=lambda: toggle_password(password, toggle_btn))
    toggle_btn.place(x=287, y=190)
    password.place(x=16, y=190)
    btn1 = tk.Button(add_email, text="Add Email",
                     font='Arial 15 bold', activebackground='#343434', activeforeground='#ffffff', borderwidth=0, command=lambda: add_db(email.get(), password.get(), listBox), padx=5, pady=3)
    btn1.place(x=140, y=250)


def delete(listBox):
    global app_list
    k = []
    for child in listBox.selection():
        k.append(listBox.item(child)["values"][0])
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    for i in k:
        c.execute("DELETE FROM emails WHERE email=:email", {
            'email': i
        })
        email_vals.remove(i)
    conn.commit()
    conn.close()
    for i in app_list.copy():
        if i[0] in k:
            app_list.remove(i)
    for record in listBox.get_children():
        listBox.delete(record)
    for i in (app_list):
        listBox.insert(parent='', index='end',
                       values=(i[0], (len(i[1])*"*")))


def play():
    play["state"] = tk.DISABLED
    info = main.get_email_info()
    try:
        recipent.delete(0, tk.END)
        recipent.insert(0, info[0])
        sub.delete(0, tk.END)
        if(info[1] != None):
            sub.insert(0, info[1])
        cc.delete(0, tk.END)
        if(info[3] != None):
            cc.insert(0, info[3])
        bcc.delete(0, tk.END)
        if(info[4] != None):
            bcc.insert(0, info[4])
        content.delete("1.0", tk.END)
        content.insert("1.0", info[2]+"\n")
    except:
        pass
    play["state"] = tk.NORMAL


def manage():
    global app_list
    app_list = []
    top = tk.Toplevel()
    top.title("Mails Manager")
    top.geometry("600x600")
    top.resizable(0, 0)
    if ("nt" == os.name):
        top.iconbitmap("./icon.ico")
    add_to_list()
    style = Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Arial", 12))
    style.configure("Treeview.Heading", font=("Arial", 16))
    style.configure('TButton', font=('Arial', 15, 'bold'),
                    borderwidth='2')
    canvas = tk.Canvas(top, width=600, height=600, bg="#070769")
    canvas.create_text(310, 30, fill="white", font="Arial 20 bold",
                       text="Mail Manager")
    cols = ('Email', 'Password')
    listBox = Treeview(canvas, columns=cols, show='headings',
                       selectmode="extended", height=18)
    listBox.column("Email", width=185, minwidth=190)
    listBox.column("Password", width=185, minwidth=190)
    for i in (app_list):
        listBox.insert(parent='', index='end', values=(i[0], (len(i[1])*"*")))
    vsb = Scrollbar(canvas, orient="vertical", command=listBox.yview)
    vsb.place(x=486, y=70, height=412)
    listBox.configure(yscrollcommand=vsb.set)
    vsb1 = Scrollbar(canvas, orient="horizontal", command=listBox.xview)
    vsb1.place(x=112, y=468, width=375)
    listBox.configure(xscrollcommand=vsb1.set)
    listBox.heading(cols[0], text=cols[0])
    listBox.heading(cols[1], text=cols[1])
    listBox.pack(padx=40, pady=70)
    canvas.pack(fill=tk.BOTH)
    canvas1 = tk.Canvas(top, bg="#070769", width=600)
    btn1 = tk.Button(canvas1, text="Add Email", width=22,
                     font='Arial 15 bold', activebackground='#343434', activeforeground='#ffffff', borderwidth=0,  command=lambda: add(listBox), padx=5, pady=3)
    btn1.grid(row=0, column=0, columnspan=4, padx=10, pady=8)
    btn2 = tk.Button(canvas1, text="Delete Email", font='Arial 15 bold',
                     width=22, activebackground='#343434', borderwidth=0, activeforeground='#ffffff', command=lambda: delete(listBox), padx=5, pady=3)
    btn2.grid(row=0, column=5, padx=10)
    canvas1.pack(expand=True, fill=tk.BOTH)


def add_attach():
    global attach_list
    filenames = filedialog.askopenfilenames(
        initialdir="/", title="Select File/Files")
    for file in filenames:
        if file != "":
            attach_list.append(file)
            listbox.insert(tk.END, file)


def del_attach():
    global attach_list
    k, s = listbox.curselection(), listbox.get(listbox.curselection())
    listbox.delete(k[0])
    attach_list.remove(s)


def send(recipent, content, sub, cc, bcc, emails):
    global attach_list
    recipent = recipent.get()
    content = content.get("1.0", "end-1c")
    subject = sub.get()
    cc = cc.get()
    bcc = bcc.get()
    sender = emails.get()

    # check_emails = [recipent, sender]
    # opt_emails = [cc, bcc]
    err = 0
    if (recipent == "" or content == ""):
        messagebox.showerror(
            "Error", "One or More Essential Text Fields are Blank!")
        err += 1
    # for email in check_emails:
    #     if (re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email) == False):
    #         messagebox.showerror("Error", "Email Format is Not Correct")
    #         err += 1
    #         break
    # for email in opt_emails:
    #     if (email != ""):
    #         if (re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email) == False):
    #             messagebox.showerror("Error", "Email Format is Not Correct")
    #             err += 1
    #             break
        
    if (err == 0):
        flag = main.send_email(recipent, subject, content,
                               sender, cc, bcc, attach_list)
        if flag:
            messagebox.showinfo("Success","The email has been sent successfully")
        elif flag==False:
            messagebox.showerror("Error","Some eroor occured, try again!")


def entered1(event):
    send_mail.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left1(event):
    send_mail.configure(
        bg="#ffffff",
        fg="#000000",
    )


def entered2(event):
    manage_mail.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left2(event):
    manage_mail.configure(
        bg="#ffffff",
        fg="#000000",
    )


def entered3(event):
    add_attach.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left3(event):
    add_attach.configure(
        bg="#ffffff",
        fg="#000000",
    )


def entered4(event):
    del_attach.configure(
        bg="#343434",
        fg="#ffffff",
    )


def left4(event):
    del_attach.configure(
        bg="#ffffff",
        fg="#000000",
    )


root = tk.Tk()
root.title('Voice Mail Client')
if "nt" == os.name:
    root.iconbitmap("icon.ico")
root.geometry("400x1010")
root.resizable(0, 0)
canvas = tk.Canvas(root, width=400, height=1010, bg="#070769")
canvas.create_text(200, 30, fill="white", font="Arial 18 bold",
                   text="Send Mails Using Voice!")
photo1 = tk.PhotoImage(file="Play.png")
tphoto1 = photo1.subsample(9, 9)
play = tk.Button(root, image=tphoto1, command=play,
                 borderwidth=0, bg="#070769", activebackground='#070769')
play.place(x=140, y=65)
canvas.create_text(114, 210, fill="white", font="Arial 12",
                   text="Enter Recipent Email/Emails")
recipent = tk.Entry(root, width=30, font="Arial 16",
                    relief="groove", borderwidth=0)
recipent.place(x=16, y=230)

canvas.create_text(62, 290, fill="white",
                   font="Arial 12", text="Enter Subject")
sub = tk.Entry(root, width=30, font="Arial 16", relief="groove", borderwidth=0)
sub.place(x=16, y=310)

canvas.create_text(83, 370, fill="white", font="Arial 12",
                   text="Enter CC (Optional)")
cc = tk.Entry(root, width=30, font="Arial 16", relief="groove", borderwidth=0)
cc.place(x=16, y=390)

canvas.create_text(90, 450, fill="white", font="Arial 12",
                   text="Enter BCC (Optional)")
bcc = tk.Entry(root, width=30, font="Arial 16", relief="groove", borderwidth=0)
bcc.place(x=16, y=470)

canvas.create_text(63, 530, fill="white",
                   font="Arial 12", text="Enter Content")
content = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, height=9, width=38, font="Arial 12", relief="groove", borderwidth=0)
content.place(x=16, y=550)


canvas.create_text(94, 740, fill="white", font="Arial 12",
                   text="Choose Sender Email")

email_vals = []
conn = sqlite3.connect('emails.db')
c = conn.cursor()
c.execute("SELECT * FROM emails")
rec = c.fetchall()
for r in rec:
    email_vals.append(r[0])
conn.commit()
conn.close()

emails = Combobox(root, values=email_vals, width=48, font="Arial 10",
                  postcommand=lambda: emails.configure(values=email_vals))
emails.current(0)
emails.place(x=16, y=760)

canvas.create_text(122, 810, fill="white",
                   font="Arial 12", text="Choose Attachments (optional)")
listbox = tk.Listbox(root, height=5, font="Arial 10",
                     width=48,
                     activestyle='dotbox')
vsb = Scrollbar(canvas, orient="vertical", command=listbox.yview)
vsb.place(x=356, y=830, height=89)
listbox.configure(yscrollcommand=vsb.set)
vsb1 = Scrollbar(canvas, orient="horizontal", command=listbox.xview)
vsb1.place(x=16, y=918, width=357)
listbox.configure(xscrollcommand=vsb1.set)
listbox.place(x=16, y=830)


del_attach = tk.Button(root, width=23, text="Delete Attachment", font="Arial 10 bold", command=del_attach,
                       activebackground='#343434', activeforeground='#ffffff', borderwidth=0)
del_attach.place(x=206, y=954)


add_attach = tk.Button(root, width=24, text="Add Attachment", font="Arial 10 bold",
                       activebackground='#343434', activeforeground='#ffffff', borderwidth=0, command=add_attach)
add_attach.place(x=5, y=954)


send_mail = tk.Button(root, width=23, text="Send Mail", font="Arial 10 bold",
                      activebackground='#343434', activeforeground='#ffffff', borderwidth=0, command=lambda: send(recipent, content, sub, cc, bcc, emails))
send_mail.place(x=206, y=980)


manage_mail = tk.Button(root, width=24, text="Manage Mails", font="Arial 10 bold",
                        activebackground='#343434', activeforeground='#ffffff', borderwidth=0, command=manage)
manage_mail.place(x=5, y=980)

send_mail.bind("<Enter>", entered1)
send_mail.bind("<Leave>", left1)
manage_mail.bind("<Enter>", entered2)
manage_mail.bind("<Leave>", left2)
add_attach.bind("<Enter>", entered3)
add_attach.bind("<Leave>", left3)
del_attach.bind("<Enter>", entered4)
del_attach.bind("<Leave>", left4)

canvas.pack(expand=True, fill=tk.BOTH)
root.mainloop()
