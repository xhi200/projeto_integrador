from tkinter import *
import pickle
from PIL import ImageTk, Image
from banco import *
from tkinter import messagebox

class Application:
    def __init__(self, master):
        master.title('Histórico de acesso')
        master.geometry('700x600')
        self.fontePadrao = ("Arial", "10")
        self.lista = StringVar()
       
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 50
        self.segundoContainer.pack()


        self.terceiroContainerA = Frame(master)
        self.terceiroContainerA["pady"] = 20
        self.terceiroContainerA.pack()


        self.terceiroContainerB = Frame(master)
        self.terceiroContainerB["pady"] = 22
        self.terceiroContainerB.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 24
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Histórico de acesso")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.lb = Listbox(self.segundoContainer, listvariable=self.lista,  width = 300)
        self.lb.pack(side=LEFT)


        self.mostra = Button(self.quartoContainer)
        self.mostra["text"] = "Mostrar Placa"
        self.mostra["font"] = ("Calibri", "8")
        self.mostra["width"] = 12
        self.mostra["command"] = self.CarregarFoto
        self.mostra.pack()

        self.consTodos = Button(self.terceiroContainerA)
        self.consTodos["text"] = "Consulta Todos"
        self.consTodos["font"] = ("Calibri", "8")
        self.consTodos["width"] = 12
        self.consTodos["command"] = self.CarregarTodos
        self.consTodos.pack()
       
        self.chave = Text(self.terceiroContainerB, height = 1, width = 12) 
        self.chave.pack(side=RIGHT)

        self.consNome = Button(self.terceiroContainerB)
        self.consNome["text"] = "Consulta Nome"
        self.consNome["font"] = ("Calibri", "8")
        self.consNome["width"] = 12
        self.consNome["command"] = self.CarregarNome
        self.consNome.pack(side=RIGHT)
        
        self.consPlaca = Button(self.terceiroContainerB)
        self.consPlaca["text"] = "Consulta Placa"
        self.consPlaca["font"] = ("Calibri", "8")
        self.consPlaca["width"] = 12
        self.consPlaca["command"] = self.CarregarPlaca
        self.consPlaca.pack()


        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

        self.figura = Label(self.quartoContainer, image = None,width=600, height=300)
        self.figura.pack()


    #Método verificar senha
    def CarregarFoto(self):
        try:
            lin = self.lb.curselection()
            elemento = self.dados[lin[0]]
            id = elemento[0]
            foto = "fts\\"+elemento[3]+"_"+str(id)+".jpg"
            #print(foto)
            quando = elemento[1]
            self.mensagem["text"] = quando
            self.mensagem.pack()
            img = ImageTk.PhotoImage(Image.open(foto))
            self.figura.configure(image=img)
            self.figura.image = img
            self.figura.pack()
        except:
            messagebox.showinfo("Aviso","Selecione uma Linha")
            
    def CarregarTodos(self):
        self.dados = ListaEVENTOS()
        lp=[]
        for elemento in self.dados:
           #print(elemento[2])
            dia =elemento[2][0]
            hora =elemento[2][1]
            diad=" "+dia[2]+"/"+dia[1]+"/"+dia[0]+" "
            horad=" "+hora[0]+":"+hora[1]+"  "
            dt=diad+horad
            lp.append((elemento[1],dt,elemento[3]))
        self.lista.set(lp)


    def CarregarPlaca(self):
        placa = self.chave.get('1.0','end')[:-1]
        self.dados= ConsultaEVENTOPlaca(placa)
        lp=[]
        for elemento in self.dados:
           #print(elemento[2])
            dia =elemento[2][0]
            hora =elemento[2][1]
            diad=" "+dia[2]+"/"+dia[1]+"/"+dia[0]+" "
            horad=" "+hora[0]+":"+hora[1]+"  "
            dt=diad+horad
            lp.append((elemento[1],dt,elemento[3]))
        self.lista.set(lp)


    def CarregarNome(self):
        nome = self.chave.get('1.0','end')[:-1]
        self.dados= ConsultaEVENTOPessoa(nome)
        lp=[]
        for elemento in self.dados:
            #print(elemento[2])
            dia =elemento[2][0]
            hora =elemento[2][1]
            diad=" "+dia[2]+"/"+dia[1]+"/"+dia[0]+" "
            horad=" "+hora[0]+":"+hora[1]+"  "
            dt=diad+horad
            lp.append((elemento[1],dt,elemento[3]))
        self.lista.set(lp)


root = Tk()
Application(root)
root.mainloop()
