import process_base
import Process_OCR
import cv2 as cv
from tkinter import filedialog, Tk
from lpr import placa
from tkinter import *
import pickle
from PIL import ImageTk, Image
from banco import *
from tkinter import messagebox
import os

class Application:
    def __init__(self, master):
        master.title('Sistema de Captura de Placas')
        master.geometry('300x200')
        self.fontePadrao = ("Arial", "10")
        self.lista = StringVar()
       
       
        self.terceiroContainerA = Frame(master)
        self.terceiroContainerA["pady"] = 10
        self.terceiroContainerA.pack()


       
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 12
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 14
        self.quintoContainer.pack()


        self.quintoBContainer = Frame(master)
        self.quintoBContainer["pady"] = 16
        self.quintoBContainer.pack()


        self.nliberar = Button(self.quintoBContainer)
        self.nliberar["text"] = "Não Liberar"
        self.nliberar["font"] = ("Calibri", "8")
        self.nliberar["width"] = 15
        self.nliberar["command"] = self.NaoLiberar
        self.nliberar["state"] = DISABLED
        self.nliberar.pack(side=RIGHT)

    
        self.liberar = Button(self.quintoBContainer)
        self.liberar["text"] = "Liberar Passagem"
        self.liberar["font"] = ("Calibri", "8")
        self.liberar["width"] = 15
        self.liberar["command"] = self.GravaEvento
        self.liberar["state"] = DISABLED
        self.liberar.pack(side=RIGHT)
     

        self.consTodos = Button(self.terceiroContainerA)
        self.consTodos["text"] = "Capturar Placa"
        self.consTodos["font"] = ("Calibri", "8")
        self.consTodos["width"] = 12
        self.consTodos["command"] = self.Capturar
        self.consTodos.pack()
       

        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
        
        self.pessoanome = Label(self.quintoContainer, text="", font=self.fontePadrao)
        self.pessoanome.pack()

    def Capturar(self):
        caminho_2 = filedialog.askopenfilename()
        imagem = cv.imread(caminho_2)

        # - Alterar escala (Nao alterar esta escala, funcionando apenas para esta resolucao)
        dimensao = (1000, 563) # Largura, Altura
        resize = cv.resize(imagem, dimensao, cv.INTER_AREA)

        cv.imshow('Foto', resize)

        # Teste Perto
        corte, selecao = placa(resize, 1)

        dimensao = (600, 200) # Largura, Altura
        corte_resize = cv.resize(corte, dimensao, cv.INTER_AREA)
        gray = cv.cvtColor(corte_resize.copy(), cv.COLOR_BGR2GRAY)

        retorno, status = Process_OCR.seg_extr_carc(gray)
    
        if status != 0:
            corte, selecao = placa(resize, 2)
            dimensao = (600, 200) # Largura, Altura
            corte_resize = cv.resize(corte, dimensao, cv.INTER_AREA)
            gray = cv.cvtColor(corte_resize.copy(), cv.COLOR_BGR2GRAY)
            retorno, status = Process_OCR.seg_extr_carc(gray)
    
        print(retorno)

        self.mensagem["text"] = retorno
        self.mensagem.pack()
        self.GravaBanco(retorno,caminho_2)
          

    def GravaBanco(self,placa,caminho):
        self.placaS=placa[0]+placa[1]+placa[2]+placa[3]+placa[4]+placa[5]+placa[6]
        pessoa = ConsultaPESSOA(self.placaS)
        self.cam=caminho
        if(pessoa==None):
            self.pessoaN="Não cadastrada"
            self.pessoanome["text"] = self.pessoaN
            self.pessoanome.pack()
            self.liberar["state"]=NORMAL
            self.nliberar["state"]=NORMAL
            self.liberar.pack()
            self.nliberar.pack()
        else:
            self.pessoaN=pessoa
            self.pessoanome["text"] = self.pessoaN
            self.pessoanome.pack()
            self.GravaEvento()
        
        
    def GravaEvento(self):
        CadastraEVENTO(self.pessoaN,self.placaS,self.cam)
        self.liberar["state"] = DISABLED
        self.nliberar["state"] = DISABLED
        self.liberar.pack()
        self.nliberar.pack()

    def NaoLiberar(self):
        self.liberar["state"] = DISABLED
        self.nliberar["state"] = DISABLED
        self.liberar.pack()
        self.nliberar.pack()


root = Tk()
Application(root)
root.mainloop()
