from ast import Lambda
from cgitb import text
from curses import nonl
from distutils.log import error
from email.mime import image
from faulthandler import disable
# from msilib.schema import File
from sqlite3 import Row
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from turtle import width
from PIL import ImageTk,Image

from click import option
from requests import head
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    # Input 3
    # variabel radio button
    input_gender = StringVar()
    label3 = Label(dframe, text="Jenis Kelamin").grid(row=2, column=0, sticky="w")
    input_laki_laki = Radiobutton(dframe, text="Laki-laki", variable=input_gender, value="Laki-laki")
    input_laki_laki.grid(row=2, column=1, padx=10, pady=10, sticky='w')
    input_perempuan = Radiobutton(dframe, text="Perempuan", variable=input_gender, value="Perempuan")
    input_perempuan.grid(row=2, column=1, padx=130, pady=10, sticky='w')
    # Input 4
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=3, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=3, column=1, padx=20, pady=10, sticky='w')
    # Input 5
    input_hobi = StringVar()
    label5 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    input5 = ttk.Combobox(dframe, textvariable=input_hobi)
    input5['values'] = ["Bernyanyi", "Main Game", "Olah Raga", "Tidur", "Menulis"]
    input5['state'] = 'readonly'
    input5.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_gender, input_jurusan, input_hobi), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jenis_kelamin, jurusan, hobi):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jenis_kelamin = jenis_kelamin.get()
    jurusan = jurusan.get()
    hobi = hobi.get()

    error_message = ""

    if(nama == ""): error_message = error_message + "Lengkapi Nama\n"
    if(nim == ""): error_message = error_message + "Lengkapi Nim\n"
    if(jenis_kelamin == ""): error_message = error_message +"Lengkapi Jenis Kelamin\n"
    if(jurusan == ""): error_message = error_message + "Lengkapi Jurusan\n"
    if(hobi == ""): error_message = error_message + "Lengkapi Hobi\n"

    if(error_message != ""):
        # Tampilkan error
        head = Label(top, text=error_message)
        head.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        btn_ok = Button(top, text="Coba Lagi", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.grid(row=1, column=1, padx=10, pady=10)
    else:
        global mydb
        global dbcursor
        query = "INSERT INTO mahasiswa (nim, nama, jenis_kelamin, jurusan, hobi) VALUES ('" + nim + "', '" + nama + "', '" + jenis_kelamin + "', '" + jurusan + "', '" + hobi + "')"
        dbcursor.execute(query)
        mydb.commit()
        # Input data disini
        head = Label(top, text="Insert Berhasil", anchor="w")
        head.pack(padx=10, pady=10)
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)

    
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=50, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=50, padx=5).grid(row=i+1, column=5)
        i += 1

def openfilename():
 
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title ='"reading_room')
    print(filename)
    return filename

# Window fasilitas kampus
def viewFasilitas():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")

    frame = LabelFrame(top, borderwidth=0, text="Fasilitas Kampus")
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    img1 = '/media/driskimaulana/New Volume/UPI/SEMESTER 4/DPBO/Python/TP3DPBO2022/python-db/images/aula.jpg'
    img2 = '/media/driskimaulana/New Volume/UPI/SEMESTER 4/DPBO/Python/TP3DPBO2022/python-db/images/lab_komputer.jpg'
    img3 = '/media/driskimaulana/New Volume/UPI/SEMESTER 4/DPBO/Python/TP3DPBO2022/python-db/images/locker.jpg'
    img4 = '/media/driskimaulana/New Volume/UPI/SEMESTER 4/DPBO/Python/TP3DPBO2022/python-db/images/perpustakaan.jpg'
    img5 = '/media/driskimaulana/New Volume/UPI/SEMESTER 4/DPBO/Python/TP3DPBO2022/python-db/images/reading_room.png'

    # list image
    image_list = [img1, img2, img3, img4, img5]

    # opens the image
    img = Image.open(img1)

    img = img.resize((250, 250), Image.ANTIALIAS)

    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
    
    # create a label
    panel = Label(frame, image = img)
     
    # set the image as img
    panel.image = img
    panel.grid(row = 1, column=0, columnspan=3)

    # fucntion back and forward
    def forward(image_index):
        nonlocal panel
        nonlocal button_back
        nonlocal button_forward
        # delete previous image
        panel.grid_forget()

        # opens the image
        img = Image.open(image_list[image_index])

        img = img.resize((250, 250), Image.ANTIALIAS)

        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
        
        # create a label
        panel = Label(frame, image = img)

        # delete button
        button_back.grid_forget()
        button_forward.grid_forget()
        
        # set the image as img
        panel.image = img
        panel.grid(row = 1, column=0, columnspan=3)

        # button 
        button_back = Button(frame, text="<<", command=lambda: back(image_index-1))
        button_forward = Button(frame, text=">>", command=lambda: forward(image_index+1))

        if image_index == 4: 
            button_forward = Button(frame, text=">>", command=lambda: forward(image_index+1), state=DISABLED)

        # show button
        button_back.grid(row=2, column=0)
        button_forward.grid(row=2, column=2)
         
    
    def back(image_index):
        nonlocal panel
        nonlocal button_back
        nonlocal button_forward
        # delete previous image
        panel.grid_forget()

        # opens the image
        img = Image.open(image_list[image_index])

        img = img.resize((250, 250), Image.ANTIALIAS)

        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
        
        # create a label
        panel = Label(frame, image = img)

        # delete button
        button_back.grid_forget()
        button_forward.grid_forget()
        
        # set the image as img
        panel.image = img
        panel.grid(row = 1, column=0, columnspan=3)

        # button 
        button_back = Button(frame, text="<<", command=lambda: back(image_index-1))
        if image_index == 0: 
            button_back = Button(frame, text="<<", command=lambda: back(image_index-1), state=DISABLED)

        button_forward = Button(frame, text=">>", command=lambda: forward(image_index+1))

        # show button
        button_back.grid(row=2, column=0)
        button_forward.grid(row=2, column=2)

    # button 
    button_back = Button(frame, text="<<", command=back, state=DISABLED)
    button_exit = Button(frame, text="Exit Program", command=root.quit)
    button_forward = Button(frame, text=">>", command=lambda: forward(1))

    # show button
    button_back.grid(row=2, column=0)
    button_exit.grid(row=2, column=1)
    button_forward.grid(row=2, column=2)

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    global mydb
    global dbcursor
    query = "DELETE FROM mahasiswa"
    dbcursor.execute(query)
    mydb.commit()
    head = Label(top, text="Delete Berhasil", anchor="w")
    head.pack(padx=10, pady=10)
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(padx=10, pady=10)


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# Fasilitas Kampus btn
b_fasilitas = Button(buttonGroup, text="Fasilitas Kampus", command=viewFasilitas, width=30)
b_fasilitas.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()