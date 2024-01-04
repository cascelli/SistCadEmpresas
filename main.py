# Projeto cadastro de empresas em Python e PySide6

''' 
- Criar um ambiente virtual 'venv' na pasta do projeto : python -m venv venv ##
- Dar um play no arquivo vazio main.py para ativar o venv no projeto
- Abrir o command palette (CTRL + SHIFT + P) (icone da engrenagem do VSCode)
  - Procurar por "Selected Interpreter" 
  - Selecionar o veenv do projeto ao invés da pasta de instalação do python na maquina
- Instalar as bibliotecas necessárias do projeto : 
   pip install pyside6
   pip install requests
   pip install pandas
   pip install openpyxl
   pip install pyinstaller
- Converter arquivos para o python
   - Arquivo icons.qrc :
      pyside6-rcc icons.qrc -o icons_rc.py
   - Arquivo cadastro.ui :
      pyside6-uic cadastro.ui -o ui_main.py
      Obs : Usando pyside2 no lugar de pyside6 - nao funcionou no Windows 7
      pyside2-uic cadastro.ui -o ui_main.py
- Icones de aplicações na internet :
   - https://icon-icons.com
- Usando pyinstaller para gerar um arquivo exe do projeto:
   - pyinstaller.exe --onefile --windowed --icon=icone.ico main.py
- Criar instalador do programa para Windows
   - https://jrsoftware.org
      baixar o innosetup-6.2.0.exe
   - Video de criacao do instalador
         
'''

from PySide6 import QtCore
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTableWidgetItem)
from ui_main import Ui_MainWindow
import sys
from ui_functions import consulta_cnpj
from database import Data_base
import pandas as pd
# Todo: Remover
import sqlite3
import os

# Classe principal MainWindow, herda as propriedades e métodos das classes :
#  QMainWindow
#  Ui_MainWindow (Janela criada - cadastro.ui que gera a classe Ui_MainWindow)

# Converter arquivo cadastro.ui para ui_main.py :
# pyside6-uic cadastro.ui -o ui_main.py
class MainWindow(QMainWindow, Ui_MainWindow):

   def __init__(self):
      super(MainWindow, self).__init__()
      self.setupUi(self)

      self.setWindowTitle("PyTax - Sistema de cadastro de empresas")
      appIcon = QIcon(u"")
      self.setWindowIcon(appIcon)

      # Define a pagina inicial
      self.pages.setCurrentWidget(self.pg_home)

      # -- Toglle Button --------------------------------------------------------------
      self.btn_toggle.clicked.connect(self.leftMenu)

      # -- Páginas do sistema ---------------------------------------------------------
      self.btn_home.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_home))
      self.btn_cadastrar.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_cadastrar))
      self.btn_sobre.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_sobre))
      self.btn_contatos.clicked.connect(lambda: self.pages.setCurrentWidget(self.pg_contatos))

      # -- Preencher automaticamente os campos do cadastro a partir dos dados obtidos com o CNPJ
      # após pressionado enter no preenchimentop do CNPJ no campo do cadastro 
      # será chamada funcao para obter os dados do mesmo a partir da API da Receita Federal
      self.txt_cnpj.editingFinished.connect(self.consult_api)

      # --- Eventos de botões ---------------------------------------------------------
      # --> Botão para executar o cadastro da empresa digitada no banco de dados
      self.btn_cadastrar_empresa.clicked.connect(self.cadastrar_empresas)
      # --> Botão para atualizar dados de empresas alteradas na tabela do aplicativo
      #    para os registros correspondentes no banco de dados
      self.btn_alterar.clicked.connect(self.update_company)
      # --> Botão de excluir registro
      self.btn_excluir.clicked.connect(self.deletar_empresa)
      # --> Botão de criar planilha do ecel
      self.btn_excel.clicked.connect(self.gerar_excel_from_table)
      #self.btn_excel.clicked.connect(self.gerar_excel_from_db)


      # Busca empresas do banco de dados e alimenta tabela
      self.buscar_empresas()

   def leftMenu(self): # define os widths do menu aberto ou fechado

      width = self.left_menu.width() # Obtem o tamanho inicial do left_menu

      if width == 9:
         newWidth = 200 # define o width do left_menu para 200
      else:
         newWidth = 9   # define o width do left_menu para 9

      # seta o frame para ser animado
      self.animation = QtCore.QPropertyAnimation(self.left_menu, b"maximumWidth")
      self.animation.setDuration(200) # Determina a duracao da animação em ms
      self.animation.setStartValue(width) 
      self.animation.setEndValue(newWidth)
      self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
      self.animation.start()

   def consult_api(self):
      # Chama funcao de consulta de cnpj na API da Receita Federal
      campos = consulta_cnpj(self.txt_cnpj.text())

      self.txt_nome.setText(campos[0])
      self.txt_logradouro.setText(campos[1])
      self.txt_numero.setText(campos[2])
      self.txt_complemento.setText(campos[3])
      self.txt_bairro.setText(campos[4])
      self.txt_municipio.setText(campos[5])
      self.txt_uf.setText(campos[6])
      self.txt_cep.setText(campos[7].replace('.','').replace('-',''))
      self.txt_telefone.setText(campos[8].replace('(','').replace(')', '').replace('-', ''))
      self.txt_email.setText(campos[9])

   def cadastrar_empresas(self):
      #print("Define db")
      db = Data_base()
      #print("conecta ao database")
      db.connect()

      #print("Define fullDataSet")
      fullDataSet = (         
         self.txt_cnpj.text(),
         self.txt_nome.text(),
         self.txt_logradouro.text(),
         self.txt_numero.text(),
         self.txt_complemento.text(),
         self.txt_bairro.text(),
         self.txt_municipio.text(),
         self.txt_uf.text(),
         self.txt_cep.text(),
         self.txt_telefone.text().strip(),
         self.txt_email.text()
      )

      # Cadastrar no banco de dados
      #print("Register_company")
      resp = db.register_company(fullDataSet)

      if resp == 'ok':
         msg = QMessageBox()
         msg.setWindowTitle("Cadastro realizado")
         msg.setText("Cadastro realizado com sucesso !")
         msg.exec()

         # Busca empresas do banco de dados e alimenta tabela
         self.buscar_empresas()

         db.close_connection()
         return
      else:
         msg = QMessageBox()
         msg.setIcon(QMessageBox.Critical)
         msg.setWindowTitle("Erro")
         msg.setText("Erro ao cadastrar.\n\nVerifique se as informações foram preenchidas corretamente.")
         msg.exec()
         db.close_connection()
         return

   def buscar_empresas(self):
      db = Data_base() # cria um objeto db
      db.connect() # conecta no db

      # Obtém os registros da tabela do banco de dados e armazena em uma lista 'result'
      result = db.select_all_companies() 

      # Limpa os dados da tabela de empresas
      self.tb_company.clearContents()
      # especifica o numero de linhas da tabela de acordo com o total de registros
      #  recuperados do banco de dados armazenados na lista 'result'
      self.tb_company.setRowCount(len(result))

      # alimenta a tabela com os itens da lista 'result'
      for row, text in enumerate(result):
         for column, data in enumerate(text):
            self.tb_company.setItem(row, column, QTableWidgetItem(str(data)))

      # Ajusta largura das colunas da tabela aos seu conteúdos
      self.tb_company.resizeColumnsToContents()  

      # Para uma unica coluna, se desejar ajustar a largura ao conteúdo,
      #  usar o indice da coluna na instrucao abaixo :
      #self.tb_company.resizeColumnToContents(indice_da_coluna_desejada)

      db.close_connection() # Encerra conexao com o banco de dados

   def update_company(self):

      dados = [] # Cria uma lista vazia
      update_dados = [] # Cria uma lista vazia

      # captura os dados da tabela de empresas em uma lista
      for row in range(self.tb_company.rowCount()): # Faz um loop lelas linhas preenchidas da tabela
         for column in range(self.tb_company.columnCount()): # Faz um loop pelas colunas da linh atual da tabela
            dados.append(self.tb_company.item(row,column).text())
         update_dados.append(dados) # acrescenta a linha na lista dados
         dados = [] # limpa a lista dados para a atualização da proxima linha da tabela

      # Atualizar dados no banco
      db = Data_base() # Cria objeto de conexão com banco de dadso
      db.connect()     # Conecta com o banco de dados

      for emp in update_dados:
         db.update_company(tuple(emp))

      db.close_connection() # Fecha conexão com banco de dadso


      # Envia mensagem de atualização ao usuario
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Information)
      msg.setWindowTitle("Atualização de dados")
      msg.setText("Dados atualizados com sucesso !")
      msg.exec()

      self.tb_company.reset()
      self.buscar_empresas()

   def deletar_empresa(self):
      db = Data_base()
      db.connect()

      # Pede confirmação antes de excluir
      msg = QMessageBox()
      msg.setWindowTitle("Excluir")
      msg.setText("Este registro será excluído")
      msg.setInformativeText("Você tem certeza que deseja excluir este registro ?")
      msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
      resp = msg.exec()

      if resp == QMessageBox.Yes:
         # Obtem o cnpj do item selecionado da tabela
         cnpj = self.tb_company.selectionModel().currentIndex().siblingAtColumn(0).data()
         # Executa exclusão do item selecionado no banco de dados
         result = db.delete_company(cnpj)
         # Atualiza tabela com empresas do banco de dados
         self.buscar_empresas()

         # Mostra mensagem de sucesso
         msg = QMessageBox()
         msg.setIcon(QMessageBox.Information)
         msg.setWindowTitle("Empresa")
         msg.setText(result)
         msg.exec()

      db.close_connection()

   def gerar_excel_from_table(self):
      dados = []
      all_dados = []

      for row in range(self.tb_company.rowCount()):
         for column in range(self.tb_company.columnCount()):
            dados.append(self.tb_company.item(row, column).text())

         all_dados.append(dados)
         dados = []

      columns = [
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
      ]

      # Cria um dataframe 
      empresas = pd.DataFrame(all_dados, columns= columns)
      empresas.to_excel("Empresas.xlsx", sheet_name = "empresas", index=False)

      # Mostra mensagem de sucesso
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Information)
      msg.setWindowTitle("Excel")
      msg.setText("Arquivo Excel gerado com sucesso !")
      msg.exec()

   def gerar_excel_from_db(self):
      # ToDo : remover cbx e buscar dados do arquivo database.py
      # remover imports de sqlite3, os
      #pastaApp=os.path.dirname(__file__)
      #nomeBanco=pastaApp+"\\sist_cad_empresas.db"
      #cnx = sqlite3.connect(nomeBanco)
      cnx = sqlite3.connect("system.db")
      empresas = pd.read_sql_query("""select * from empresas""", cnx)
      empresas.to_excel("Empresas.xlsx", sheet_name = "empresas", index=False)

      # Mostra mensagem de sucesso
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Information)
      msg.setWindowTitle("Excel")
      msg.setText("Arquivo Excel gerado com sucesso !")
      msg.exec()


# Se este arquivo que estiver sendo executado diretamente, 
#   rode o bloco de código dentro do "if" abaixo
#      
# https://www.youtube.com/watch?v=150-dpYG1pg

if(__name__ == "__main__"):

   # Cria tabela no banco de dados, se não existir
   db = Data_base()
   db.connect()
   db.create_table_company()
   db.close_connection()

   # Define aplicação e a executa
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()
