import matplotlib
matplotlib.use('TkAgg')

from Tkinter import *
import Tkinter as tk
import time
from datetime import datetime
from PIL import ImageTk, Image
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
        self.text = "Waiting"
        self.w = Label(self.window, text=self.text,font=("Helvetica", 20))
        self.w.grid(row = 4, columnspan = 1)
        # w.pack()

    def refreshText(self,text):
        self.w = Label(self.window, text=text ,font=("Helvetica", 20))
        self.w.grid(row = 4, columnspan = 1)

    #Loop do codigo
    def iniciar(self):
        self.window.mainloop()

    #Acoes dos botoes
    def Receive(self):
        self.refreshText("Receiving")
        time.sleep(0.3)
        self.refreshText(Server.main())

    def Send(self):
        self.refreshText("Sending")
        time.sleep(0.3)
        self.refreshText(Client.main())

    

#Loop do codigo
app = Janela_Principal()
app.iniciar()
