import sqlite3
from sqlite3 import Error
#import os

#import pydoc
#import pyodbc.Error 

#pastaApp=os.path.dirname(__file__)
##nomeBanco=pastaApp+"\\system.db"
#nomeBanco=pastaApp+"\\sist_cad_empresas.db"

class Data_base():

    def __init__(self, name = "system.db") -> None:
    #def __init__(self, name = nomeBanco) -> None:
        self.name = name

    def connect(self):
        try: 
            self.connection = sqlite3.connect(self.name)
        except Error as ex:
            print(ex)

    def close_connection(self):
        try:
            self.connection.close()
        except Error as ex:
            print(ex)
            pass

    def create_table_company(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """ 
                    create table if not exists empresas (
                        cnpj text,
                        nome text, 
                        logradouro text, 
                        numero text,
                        complemento text,
                        bairro text,
                        municipio text,
                        uf text,
                        cep text,
                        telefone text,
                        email text,

                        primary key (cnpj)
                    );
                """
            )
        except Error as ex:
            print(ex)
            pass

    def register_company(self, fullDataSet):
        #print("Funcao register_compay")

        #print("campos_tabela")
        campos_tabela = (
            'cnpj',
            'nome', 
            'logradouro', 
            'numero',
            'complemento',
            'bairro',
            'municipio',
            'uf',
            'cep',
            'telefone',
            'email'
        )

        #print("qtd")
        #qtd = ('?,?,?,?,?,?,?,?,?,?,?')
        qtd = ','.join(map(str, '?'*11)) # Mesmo que a instrucao anterior
        #qtd = ','.join(map(str, '?'*2)) # Mesmo que a instrucao anterior

        #print("self.connection.cursor")
        cursor = self.connection.cursor()

        #print("fullDataSet:\n")
        #print(fullDataSet)
        #print("\n")
        ##print(f"cnpj: {fullDataSet[0]}\n")
        ##print(f"nome: {fullDataSet[1]}\n")

        try:
            #print("cursor.execute()")

            #print(f"Values : {qtd}")
            query = f"""insert into empresas {campos_tabela} values ({qtd})"""

            #print(f"query : {query}\n")
            #print (f"tuple(fullDataSet) : {tuple(fullDataSet)}")
            ##print (f"tuple(fullDataSet) : {tuple(fullDataSet[0], fullDataSet[1])}")

            cursor.execute(query, tuple(fullDataSet))
            #cursor.execute(query, tuple(fullDataSet[0], fullDataSet[1]))

            #print("commit")
            self.connection.commit()
            return ("ok")
        
        except Error as ex:
            print(ex)
            return "Erro"

    def select_all_companies(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("select * from empresas order by nome")
            empresas = cursor.fetchall()    
            return empresas
        except Error as ex:
            print(ex)
            pass

    def delete_company(self, id):

        #print(f"Excluir cnpj : {id}")

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"delete from empresas where cnpj = '{id}'")
            #empresas = cursor.commit()
            self.connection.commit()
            return "Cadastro de empresa excuido com sucesso !"    
        except Error as ex:
            print(ex)
            return "Erro ao excluir registro !"

    def update_company(self, fullDataSet):

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """ 
                    update empresas set

                    cnpj = '{fullDataSet[0]}',
                    nome = '{fullDataSet[1]}',
                    logradouro = '{fullDataSet[2]}',
                    numero = '{fullDataSet[3]}',
                    complemento = '{fullDataSet[4]}',
                    bairro = '{fullDataSet[5]}',
                    municipio = '{fullDataSet[6]}',
                    uf = '{fullDataSet[7]}',
                    cep = '{fullDataSet[8]}',
                    telefone = '{fullDataSet[9]}',
                    email = '{fullDataSet[10]}'

                    where cnpj = '{fullDataSet[0]}'
                """
            )
            self.connection.commit()

            return f"Cadastro de empresa de CNPJ : {fullDataSet[0]} atualizado com sucesso !"

        #except pyodbc.Error as ex: 
        #    sqlstate = ex.args[1] # Seleciona o códigoe a descrição do erro
        #    print(sqlstate)

        except Error as ex:
            print(ex)
            return "Erro ao atualizar empresa de CNPJ : {fullDataSet[0]} !"
