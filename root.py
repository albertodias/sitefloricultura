''' DEUS SEJA LOUVADO - ALBERTO DIAS 14/11/2024 AS 11:48 HS '''

''' Bibliotecas '''
import logging
import sqlite3
import webbrowser
import base64
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from datetime import time
from ast import Try
from time import localtime
import time
import tkinter as tk
from tkinter import (END, Tk, Button, Frame, Entry, Label, ttk, Scrollbar, Menu, Canvas, StringVar, OptionMenu, messagebox, Toplevel)
logging.basicConfig(level=logging.INFO, filename='execucao.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# #####################################################################

''' Inicio root '''
root = tk.Tk()

''' Classe das Funçoes '''

''' Classe Validadores '''


class Validadores():
    def validate_entry2(self, text):
        if text == '':
            return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100


''' Classe Gradiente para o Frame '''


class GradientFrame(Canvas):
    def __init__(self, parent, color1='#C6CCFF', color2='gray35', **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind('<Configure>', self._draw_gradiente)

    def _draw_gradiente(self, event):
        self.delete('gradient')
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = '#%4.4x%4.4x%4.4x' % (nr, ng, nb)
            self.create_line(i, 0, i, height, tags=('gradient,'), fill=color)
            self.lower('gradient')


''' Classe relatórios em PDf '''


class Relatorios():
    def printCliente(self):
        # Abrindo o relatorio no webbrowser
        webbrowser.open('cliente.pdf')

    def geraRelatCliente(self):
        # Gerando o Relatorio
        self.c = canvas.Canvas('cliente.pdf')
        # Capturando as Informaçoes na Tela
        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.foneRel = self.fone_entry.get()
        self.cidadeRel = self.cidade_entry.get()
        # preparando o relatorio
        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')
        self.c.setFont('Helvetica-Bold', 18)
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 670, 'Nome:   ')
        self.c.drawString(50, 630, 'Fone:   ')
        self.c.drawString(50, 600, 'Cidade: ')
        self.c.setFont('Helvetica', 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.cidadeRel)
        # Insirindo um retangulo
        self.c.rect(20, 775, 550, 45, fill=False, stroke=True)
        self.c.rect(20, 550, 550, 215, fill=False, stroke=True)
        self.c.showPage()
        self.c.save()
        self.printCliente()

# Classe Funcs - Varias Funcoes do Programa


class Funcs():
    # Funcao para limpar a tela de digitacao
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    # Funcao para se conectar ao banco de dados SQlite3

    def conecta_db(self):
        self.conn = sqlite3.connect('clientes.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    # Funcao para se desconectar ao Banco de Dados

    def desconecta_db(self):
        self.conn.close()
    # Funcao para se criar as tabelas do Banco de Dados

    def montaTabelas(self):
        # Usando o try para se operar no Banco de dados
        try:
            self.conecta_db()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes
                    (codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome CHAR(40) NOT NULL,
                    fone CHAR(40),
                    cidade CHAR(40));
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            # Gravando o erro se nao foi possivel criar a tabela clientes
            logging.info(f"Erro ao criar tabela clientes {e}")
        # Desconectando da Tabela
        self.desconecta_db()

    def variaveis(self):
        # Capturando as informações digitadas pelo operador
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()

    def add_cliente(self):
        # Importando as variaveis
        self.variaveis()
        # Verificando se o campo nome foi preenchido, se não dá um aviso ao operador
        if self.nome_entry.get() == '':
            msg = ('Para cadastrar é necessário que o nome esteja preenchido !')
            messagebox.showinfo('Cadastro de Clientes - Aviso', msg)
        else:
            ...

        # Transformando as informações para maisculo, nome e cidade
        self.nome = self.nome.upper()
        self.cidade = self.cidade.upper()
        # Insere um dado novo se pelo menos o nome esta preenchido
        if self.nome != '':
            # Inserindo um novo cliente no cadastro
            try:
                self.conecta_db()
                self.cursor.execute(
                    """ INSERT INTO clientes (nome, fone, cidade)
                    VALUES(?, ?, ?) """, (self.nome, self.fone, self.cidade)
                )

                self.conn.commit()
            except sqlite3.Error as e:
                # Gravando o erro se nao foi possivel inserir na tabela clientes
                logging.info(f"Erro ao inserir dados na tabela clientes {e}")
            # Desconectando da Tabela
            self.desconecta_db()
            # Preenchendo a Lista de Clientes
            self.select_lista()
            # Chameando a funcao para limpar a tela
            self.limpa_tela()
            # Setando o focus no campo nome
            self.nome_entry.focus()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        # Capturando a lista de clientes para exibicao
        try:
            self.conecta_db()
            lista = self.cursor.execute(
                """ SELECT codigo, nome, fone, cidade FROM clientes ORDER BY nome ASC ; """)
            for i in lista:
                self.listaCli.insert("", END, values=i)

        except sqlite3.Error as e:
            # Gravando o erro se nao foi possivel criar a tabela clientes
            logging.info(f"Erro ao consultar a tabela clientes {e}")
        # Desconectando da Tabela
        self.desconecta_db()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()
        # Preenche os campos editaveis para poder ou alterar
        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)

    def deleta_cliente(self):
        # Capturando a informação para delecao
        self.codigo = self.codigo_entry.get()
        delecao = self.codigo
        if delecao != '':
            # Deletando um cliente do registro no cadastro
            try:
                self.conecta_db()
                self.cursor.execute(
                    """ DELETE FROM clientes WHERE codigo = ? """, (delecao,))
                self.conn.commit()
            except sqlite3.Error as e:
                # Gravando o erro se nao foi possivel criar a tabela clientes
                logging.info(f"Erro ao deletar na tabela clientes {e}")
            # Desconectando da Tabela
            self.desconecta_db()
            # Preenchendo a Lista de Clientes
            self.select_lista()
            # Chameando a funcao para limpar a tela
            self.limpa_tela()
            # Setando o focus no campo nome
            self.nome_entry.focus()

    def altera_cliente(self):
        self.variaveis()
        # Transformando as informações para maisculo, nome e cidade
        self.nome = self.nome.upper()
        self.cidade = self.cidade.upper()
        try:
            self.conecta_db()
            self.cursor.execute(
                """ UPDATE clientes SET nome = ?, fone = ?, cidade = ?
                WHERE codigo = ? """, (self.nome, self.fone, self.cidade, self.codigo)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            # Gravando o erro se nao foi possivel alterar a tabela clientes
            logging.info(f"Erro ao alterar na tabela clientes {e}")
        # Desconectando da Tabela
        self.desconecta_db()
        # Preenchendo a Lista de Clientes
        self.select_lista()
        # Chameando a funcao para limpar a tela
        self.limpa_tela()
        # Setando o focus no campo nome
        self.nome_entry.focus()

    def busca_cliente(self):
        # Transformando as informações
        self.nome_entry.insert(END, '%')
        busca = self.nome_entry.get()
        # limpando a listagem de  clientes
        self.listaCli.delete(*self.listaCli.get_children())
        # Pesquisando um cliente no Banco de Dados
        try:
            self.conecta_db()
            lista = self.cursor.execute(
                """ SELECT codigo, nome, fone, cidade FROM clientes
                    WHERE nome LIKE '%s' ORDER BY nome ASC """ % busca)
            for i in lista:
                self.listaCli.insert("", END, values=i)

        except sqlite3.Error as e:
            # Gravando o erro se nao foi possivel pesquisar na tabela clientes
            logging.info(f"Erro ao pesquisar na tabela clientes {e}")
        # Desconectando da Tabela
        self.desconecta_db()
        # Chameando a funcao para limpar a tela
        self.limpa_tela()
        # Setando o focus no campo nome
        self.nome_entry.focus()

    def images_base64(self):
        # self.botao_base64 = ''  # codificado no site base64.guru
        pass

    # Mutiplas Janelas - Definindo a Janela 2
    def Janela2(self):
        self.root2 = Toplevel()
        self.root2.title('janela 2 (testes)')
        self.root2.configure(background='lightblue')
        self.root2.geometry('400x200')
        self.root2.resizable(True, True)
        self.root2.transient(self.root)  # De que janela partiu esta janela
        self.root2.focus_force()  # Setando o focus na Janela 2
        self.root2.grab_set()    # Força que nao pode digitar em outra janela


''' Classe Application (Principal)'''


class Application(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.root = root
        self.images_base64()  # Empacotando as imagens que o programa precisa
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        self.nome_entry.focus()  # setando o focus no campo nome
        '''Looping'''
        root.mainloop()

    def tela(self):
        self.root.title('Cadastro de Clientes')
        self.root.configure(background='#1e3743')
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6',
                             highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6',
                             highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # ########################################################################
        # criação do botao canvas
        # self.canvas_bt = Canvas(self.frame_1, bd=0, bg='#1e3743',
        #                        highlightbackground='gray', highlightthickness=5)
        # self.canvas_bt.place(relx=0.19, rely=0.08,
        #                     relwidth=0.24, relheight=0.19)
        # ########################################################################

        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = GradientFrame(self.abas, 'white', 'blue')  # Antigo Frame
        self.aba2 = GradientFrame(self.abas, 'white', 'green')  # Antigo Frame

        self.aba1.configure(background='#dfe3ee')
        self.aba2.configure(background='lightgray')

        self.abas.add(self.aba1, text='Basicos')
        self.abas.add(self.aba2, text='Extras')

        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        # Criação do botão limpar
        self.bt_limpar = Button(self.aba1, text='Limpa', bd=2, bg='#107db2',
                                activebackground='#108ecb', activeforeground='white',
                                fg='white', font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        # Criação do botão buscar
        self.bt_buscar = Button(self.aba1, text='Busca', bd=2,
                                bg='#107db2', fg='white',
                                activebackground='#108ecb', activeforeground='white',
                                font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.32, rely=0.1, relwidth=0.1, relheight=0.15)

        # self.balao_buscar = tix.Balloon(self.frame_1)
        # self.balao_buscar.bind_widget(self.bt_buscar, baloonmsg="Digite no campo nome o cliente que deseja pesquisar ")

        # Criação do botão novo
        self.bt_novo = Button(self.aba1, text='Novo', bd=2,
                              bg='#107db2', fg='white',
                              activebackground='#108ecb', activeforeground='white',
                              font=('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        # Criação do botão alterar
        self.bt_alterar = Button(self.aba1, text='Altera', bd=2,
                                 bg='#107db2', fg='white',
                                 activebackground='#108ecb', activeforeground='white',
                                 font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.72, rely=0.1,
                              relwidth=0.1, relheight=0.15)
        # Criação do botão apagar
        self.bt_apagar = Button(self.aba1, text='Apaga', bd=2,
                                bg='#107db2', fg='white',
                                activebackground='#108ecb', activeforeground='white',
                                font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.84, rely=0.1, relwidth=0.1, relheight=0.15)
        # criação da label do codigo
        self.lb_codigo = Label(self.aba1, text='Código',
                               bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)
        # criacao da entrada do codigo
        self.codigo_entry = Entry(self.aba1, bg="#dfe3ee", fg='#107db2')
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)
        # criação da label do Nome
        self.lb_nome = Label(self.aba1, text='Nome',
                             bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)
        # criacao da entrada do Nome
        self.nome_entry = Entry(self.aba1, relief='groove')
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)
        # criação da label do Telefone
        self.lb_fone = Label(self.aba1, text='Fone',
                             bg='#dfe3ee', fg='#107db2')
        self.lb_fone.place(relx=0.05, rely=0.6)
        # criacao da entrada do Telefone
        self.fone_entry = Entry(self.aba1, relief='groove')
        self.fone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)
        # criação da label do Cidade
        self.lb_cidade = Label(self.aba1, text='Cidade',
                               bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.6)
        # criacao da entrada da Cidade
        self.cidade_entry = Entry(self.aba1, relief='groove')
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)

        # Drop Down Button
        self.Tipvar = StringVar()
        self.Tipv = ('Solteiro(a)', 'Casado(a)',
                     'Divorciado(a)', 'Viuvo(a)', 'Separado(a)')
        self.Tipvar.set('Solterio(a)')
        self.popupMenu = OptionMenu(self.aba2, self.Tipvar, *self.Tipv)
        self.popupMenu.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.2)
        self.estado_civil = self.Tipvar.get()
        print(self.estado_civil)

    def lista_frame2(self):
        # Criando uma lista no Frame2 com as colunas
        self.listaCli = ttk.Treeview(
            self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4'))
        # Cabeçario das Colunas
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Cod')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Fone')
        self.listaCli.heading('#4', text='Cidade')
        # Tamanho do cabeçario das Colunas = Soma teme que dar 500
        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=29)
        self.listaCli.column('#2', width=170)
        self.listaCli.column('#3', width=100)
        self.listaCli.column('#4', width=200)
        # Posicionando a lista no frame2
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        # Incluindo a Barra de Rolagem
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1,
                               relwidth=0.04, relheight=0.85)
        self.listaCli.bind('<Double-1>', self.OnDoubleClick)

    def Menus(self):
        # definindo o menu principal
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        filemenu3 = Menu(menubar)
        # Criando uma funcao para ser usada no menu
        def Quit(): self.root.destroy()
        # colocando as abas no menu como: opcoes
        menubar.add_cascade(label='Opções', menu=filemenu)
        menubar.add_cascade(label='Relatórios', menu=filemenu2)
        menubar.add_cascade(label='Login', menu=filemenu)
        menubar.add_cascade(label='Sobre', menu=filemenu3)
        # colocando as opcoes no menu
        filemenu.add_command(label='Sair', command=Quit)
        filemenu.add_command(label='Limpa Cliente', command=self.limpa_tela)
        filemenu2.add_command(label='Ficha do Cliente',
                              command=self.geraRelatCliente)
        filemenu.add_command(label='Login', command=self.Janela2)

    def validaEntradas(self):
        self.vcmd2 = (self.root.register(self.validate_entry2), '%P')


''' Executando '''
Application()
''' Fim deste modulo '''
