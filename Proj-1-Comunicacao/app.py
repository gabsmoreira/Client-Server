import matplotlib
matplotlib.use('TkAgg')

from Tkinter import *
import Tkinter as tk
import time
from datetime import datetime
from PIL import ImageTk, Image
from tkinter import filedialog
import Client
import Server

class Janela_Principal():

    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry("298x298+100+100")
        self.window.title("GATONET")
        self.window.configure(background = 'white')
        self.window.resizable(False, False)

        # Geometria da pagina
        self.window.rowconfigure(0, minsize = 100)
        self.window.rowconfigure(1, minsize = 10)
        self.window.rowconfigure(2, minsize = 10)
        self.window.rowconfigure(3, minsize = 10)
        self.window.rowconfigure(4, minsize = 10)
        self.window.rowconfigure(5, minsize = 10)
        self.window.columnconfigure(0, minsize = 10)
        self.window.columnconfigure(1, minsize = 10)




        #Label
        self.Logo = ImageTk.PhotoImage(Image.open("cat.jpg"))
        self.Logo_label = tk.Label(self.window, image = self.Logo, height = 1, width = 1)
        self.Logo_label.grid(row = 0, column = 0, sticky = "nsew")


        #Botoes
        self.button_treinar = tk.Button(self.window, text = "SEND", height = 3, width = 30)
        self.button_treinar.grid(row = 1, columnspan = 1)
        self.button_treinar.configure(command = self.Send)

        self.button_Reconhecimento = tk.Button(self.window, text = "RECEIVE", height = 3, width = 30)
        self.button_Reconhecimento.grid(row   = 2, columnspan = 1)
        self.button_Reconhecimento.configure(command = self.Receive)

        # self.button_des = tk.Text(self.window, text = "Disconnect", height = 3, width = 30)
        # self.button_des.grid(row = 3, columnspan = 1)
        # self.button_des.configure(command = self.Send)

        self.var = StringVar(self.window)
        self.var.set("Choose your port") # initial value

        self.option = OptionMenu(self.window, self.var, "/dev/cu.usbmodem1461","/dev/cu.usbmodem1451", "/dev/cu.usbmodem1441", "/dev/cu.usbmodem1431", "/dev/cu.usbmodem1411","/dev/ttyACM0","/dev/ttyACM1","COM1","COM2","COM3","COM4","COM5","COM6" )
        self.option.grid(row   = 4)

        self.text = "Waiting"
        self.w = Label(self.window, text=self.text,font=("Helvetica", 20))
        self.w.grid(row = 5, columnspan = 1)
        # w.pack()

    def refreshText(self,text):
        self.w = Label(self.window, text=text ,font=("Helvetica", 20))
        self.w.grid(row = 5, columnspan = 1)

    #Loop do codigo
    def iniciar(self):
        self.window.mainloop()

    #Acoes dos botoes
    def Receive(self):
        self.refreshText("Receiving")
        time.sleep(0.3)
        self.refreshText(Server.main(self.var.get()))

    def Send(self):
        print(self.var.get())
        self.window.filename = filedialog.askopenfilename()
        self.refreshText("Sending")
        time.sleep(0.3)
        self.refreshText(Client.main(self.window.filename,self.var.get()))


#Loop do codigo
app = Janela_Principal()
app.iniciar()
