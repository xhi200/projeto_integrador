from tkinter import *
import pickle
from PIL import ImageTk, Image
from banco import *
from tkinter import messagebox

class Application:
    def __init__(self, master):
        master.title('Cadastro veículos')
        master.geometry('400x200')
        self.fontePadrao = ("Arial", "10")
        self.lista = StringVar()
       
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 50
        self.segundoContainer.pack()


        self.terceiroContainer = Frame(master)
        self.terceiroContainer["pady"] = 20
        self.terceiroContainer.pack()


        self.nome = Label(self.primeiroContainer, text="Nome do motorista")
        self.nome["font"] = ("Arial", "10", "bold")
        self.nome.pack()


        self.placa = Label(self.segundoContainer, text="Placa do Veículo")
        self.placa["font"] = ("Arial", "10", "bold")
        self.placa.pack()

        self.mostra = Button(self.terceiroContainer)
        self.mostra["text"] = "Gravar"
        self.mostra["font"] = ("Calibri", "8")
        self.mostra["width"] = 12
        self.mostra["command"] = self.Gravar
        self.mostra.pack()

        self.tnome = Text(self.primeiroContainer, height = 1, width = 12) 
        self.tnome.pack(side=RIGHT)
        
        self.tplaca = Text(self.segundoContainer, height = 1, width = 12) 
        self.tplaca.pack(side=RIGHT)



    def Gravar(self):
        nome = self.tnome.get('1.0','end')[:-1]
        placa = self.tplaca.get('1.0','end')[:-1]
        #print(nome,placa)
        self.tplaca.delete('1.0', END)
        self.tnome.delete('1.0', END)
        CadastraPESSOA(nome,placa)

root = Tk()
Application(root)
root.mainloop()
