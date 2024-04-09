import datetime
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar

from tarefa_data import TarefaData
from tarefa_model import Tarefa


class App:
    def __init__(self):
        self.db = TarefaData()

        self.janela = Tk()
        self.janela.title("Lista de tarefas")
        self.janela.iconbitmap('icone.ico')

        Label(self.janela, text="Descrição da Tarefa:", font=("Arial", 16)).grid(row=0, column=0)
        self.entrada_descricao = Text(self.janela, wrap=WORD, width=30, height=2)
        self.entrada_descricao.grid(row=0, column=1, padx=10, pady=50, sticky="w")

        Label(text="Data de Início: ", font=("Arial", 14)).grid(row=2, column=0)
        self.entrada_data_inicio = Calendar(self.janela, selectmode="day", date_pattern="yyyy-mm-dd")
        self.entrada_data_inicio.grid(row=3, column=0, padx=40)

        Label(text="Data de Término: ", font=("Arial", 14)).grid(row=2, column=1)
        self.entrada_data_termino = Calendar(self.janela, selectmode="day", date_pattern="yyyy-mm-dd")
        self.entrada_data_termino.grid(row=3, column=1)

        Label(self.janela, text="Status da Tarefa: ", font=("Arial", 16)).grid(row=4, column=0)
        self.status = ["A fazer", "Em andamento", "Finalizada"]
        self.entrada_status = ttk.Combobox(self.janela, width=30, height=2, values=self.status)
        self.entrada_status.grid(row=4, column=1, pady=40)

        Button(self.janela, text="Adicionar Tarefa", command=self.inserir_tarefa).grid(row=6, column=0 ,padx=10, pady=10)
        Button(self.janela, text="Excluir Tarefa",background='red', command=self.excluir_tarefa).grid(row=6, column=1, padx=10, pady=10)
        Button(self.janela, text="Marcar como concluída", command=self.marcar_concluida).grid(row=6, column=3, padx=10, pady=10)


        self.frame = Frame(self.janela)
        self.frame.grid(row=5, column=0, columnspan=4)

        self.colunas = ['Descrição', 'Data de Início', 'Data de Término', 'Status']
        self.tabela = ttk.Treeview(self.frame, columns=self.colunas, show='headings')
        for coluna in self.colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=200)
        self.tabela.pack()

        self.tabela.bind('<ButtonRelease-1>', self.selecionar_tarefa)

        self.atualizar_tabela()
        self.janela.mainloop()

    def selecionar_tarefa(self, event):
        item = self.tabela.selection()
        if item:
            descricao = self.tabela.item(item, 'values')[0]
            data_inicio = self.tabela.item(item, 'values')[1]
            data_termino = self.tabela.item(item, 'values')[2]
            status = self.tabela.item(item, 'values')[3]

    def atualizar_tabela(self):
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        tarefas = self.db.obter_tarefas()

        for tarefa in tarefas:
            self.tabela.insert('', 'end', values=(
                tarefa.descricao, tarefa.data_inicio, tarefa.data_termino, tarefa.status_tarefa
            ))

    def marcar_concluida(self):
        item = self.tabela.selection()
        if item:
            descricao = self.tabela.item(item, 'values')[0]
            self.db.marcar_concluida(descricao)
            self.atualizar_tabela()
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para marcar como concluída.")

    def criar_tarefa(self):
        descricao = self.entrada_descricao.get("1.0", END).strip()
        data_inicio_raw = self.entrada_data_inicio.get_date()
        data_inicio = datetime.datetime.strptime(data_inicio_raw, "%Y-%m-%d")
        data_termino_raw = self.entrada_data_termino.get_date()
        data_termino = datetime.datetime.strptime(data_termino_raw, "%Y-%m-%d")
        status = self.entrada_status.get()
        tarefa = Tarefa(descricao, data_inicio, data_termino, status)
        return tarefa

    def inserir_tarefa(self):
        tarefa = self.criar_tarefa()
        self.db.inserir_tarefa(tarefa)
        self.atualizar_tabela()
        messagebox.showinfo("Aviso", "Tarefa inserida com sucesso")

    def excluir_tarefa(self):
        item = self.tabela.selection()
        if item:
            descricao = self.tabela.item(item, 'values')[0]
            self.db.excluir_tarefa(descricao)
            self.atualizar_tabela()
            messagebox.showinfo("Aviso", "Tarefa excluída com sucesso")
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")


if __name__ == "__main__":
    app = App()
