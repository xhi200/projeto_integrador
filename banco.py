import sqlite3
import datetime

def CriaTabelaLOG():
    try:
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlite_create_table_query = '''CREATE TABLE eventos (
                                       id INTEGER PRIMARY KEY autoincrement,
                                       nome TEXT NOT NULL,
                                       placa TEXT NOT NULL,
                                       foto BLOB,
                                       quando timestamp);'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        cursor.close()

    except sqlite3.Error as error:
        print("Tabela já existe")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def CriaTabelaPESSOAS():
    try:
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlite_create_table_query = '''CREATE TABLE pessoas (
                                       id INTEGER PRIMARY KEY autoincrement,
                                       nome TEXT NOT NULL,
                                       placa TEXT NOT NULL);'''

        cursor = sqliteConnection.cursor()
        cursor.execute(sqlite_create_table_query)
        cursor.close()

    except sqlite3.Error as error:
        print("Tabela já existe")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    try:
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    except:
      print("problema em converter")  

def CadastraEVENTO(nome, placa, foto):
    try:
        quando = datetime.datetime.now()
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlTexto = """INSERT INTO 'eventos'
                          ('nome', 'quando','placa','foto') 
                          VALUES (?, ?, ?, ?);"""

        
        empFoto = convertToBinaryData(foto)
        sqlTupla = (nome, quando, placa,empFoto)
        cursor.execute(sqlTexto, sqlTupla)
        sqliteConnection.commit()
        #print("Adicionando OK \n")

    except sqlite3.Error as error:
        print("Erro no cadastro", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def CadastraPESSOA(nome, placa):
    try:
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlTexto = """INSERT INTO 'pessoas'
                          ('nome', 'placa') 
                          VALUES (?, ?);"""

        sqlTupla = (nome, placa)
        cursor.execute(sqlTexto, sqlTupla)
        sqliteConnection.commit()
        #print("Adicionando OK \n")

    except sqlite3.Error as error:
        print("Erro no cadastro", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def writeTofile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


def ListaEVENTOS():
    try:
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")
        vet=[]
        
        sqlite_select_query = """SELECT id, nome, quando, placa, foto from eventos"""
        cursor.execute(sqlite_select_query)
        registros = cursor.fetchall()

        for linha in registros:
            idEvento   = linha[0]
            nomeEvento = linha[1]
            dataEvento = linha[2]
            placa = linha[3]
            foto = linha[4]
            fotoPath =  "fts\\"+placa+"_"+str(idEvento)+".jpg"
            writeTofile(foto, fotoPath)
        #    print(idEvento," - ",nomeEvento," adicionado em ", dataEvento," placa: ",placa)
            data = (dataEvento.split(' ')[0].split('-'), dataEvento.split(' ')[1].split(':'))
        #    print(data)
            item=(idEvento,nomeEvento,data,placa,fotoPath)
            vet.append(item)
         
        cursor.close()
        return vet
    
    except sqlite3.Error as error:
        print("Error na consulta", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def ConsultaEVENTOPessoa(nome):
    try:
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlite_select_query = """SELECT id, nome, quando, placa, foto from eventos where nome=?"""
        cursor.execute(sqlite_select_query,(nome,))
        registros = cursor.fetchall()
        vet=[]
        
        for linha in registros:
            idEvento   = linha[0]
            nomeEvento = linha[1]
            dataEvento = linha[2]
            placa = linha[3]
            foto = linha[4]
            fotoPath =  "fts\\"+placa+"_"+str(idEvento)+".jpg"
            writeTofile(foto, fotoPath)
         #   print(idEvento," - ",nomeEvento," adicionado em ", dataEvento," placa: ",placa)
            data = (dataEvento.split(' ')[0].split('-'), dataEvento.split(' ')[1].split(':'))
          #  print(data)
            item=(idEvento,nomeEvento,data,placa,fotoPath)
            vet.append(item)
         
        cursor.close()
        return vet
    
    except sqlite3.Error as error:
        print("Error na consulta", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def ConsultaEVENTOPlaca(placa):
    try:
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlite_select_query = """SELECT id, nome, quando, placa, foto from eventos where placa=?"""
        cursor.execute(sqlite_select_query,(placa,))
        registros = cursor.fetchall()
        vet=[]
        for linha in registros:
            idEvento   = linha[0]
            nomeEvento = linha[1]
            dataEvento = linha[2]
            placa = linha[3]
            foto = linha[4]
            fotoPath =  "fts\\"+placa+"_"+str(idEvento)+".jpg"
            writeTofile(foto, fotoPath)
          #  print(idEvento," - ",nomeEvento," adicionado em ", dataEvento," placa: ",placa)
            data = (dataEvento.split(' ')[0].split('-'), dataEvento.split(' ')[1].split(':'))
            item=(idEvento,nomeEvento,data,placa,fotoPath)
            vet.append(item)
         #   print(data)

        cursor.close()
        return vet
    
    except sqlite3.Error as error:
        print("Error na consulta", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()



def ConsultaPESSOA(placa):
    try:
        nomePes=None
        sqliteConnection = sqlite3.connect('tabx.db')
        cursor = sqliteConnection.cursor()
        #print("Conectado")

        sqlite_select_query = """SELECT id, nome,  placa from pessoas where placa=?"""
        cursor.execute(sqlite_select_query,(placa,))
        registros = cursor.fetchall()

        for linha in registros:
            idPes   = linha[0]
            nomePes = linha[1]
            placa = linha[2]
        #    print(idPes," - ",nomePes,"  placa: ",placa)
        
        cursor.close()
        return  nomePes
    
    except sqlite3.Error as error:
        print("Error na consulta", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

