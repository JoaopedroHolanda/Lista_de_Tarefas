import datetime
from tkinter import messagebox
import pymysql.cursors
from tarefa_model import Tarefa

class TarefaData:
    def __init__(self):
        try:
            self.conexao = pymysql.connect(
                user='root',
                host='localhost',
                password='12345678',
                database='lista_tarefas',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conexao.cursor()

        except Exception as error:
            print(f"Erro ao conectar com o banco: Erro: {error}")

    def obter_tarefas(self):
        try:
            self.cursor.execute("SELECT * FROM tarefas")
            tarefas = []
            for row in self.cursor.fetchall():
                tarefas.append(Tarefa(row['descricao'], row['data_inicio'], row['data_termino'], row['status_tarefa']))
            return tarefas
        except Exception as error:
            print(f"Erro ao obter as tarefas: {error}")


    def inserir_tarefa(self, tarefa: Tarefa):
        try:
            sql = 'INSERT INTO tarefas(descricao,data_inicio,data_termino,status_tarefa) VALUES(%s,%s,%s,%s)'
            data_inicio = tarefa.data_inicio.strftime('%Y-%m-%d')
            data_termino = tarefa.data_termino.strftime('%Y-%m-%d')
            self.cursor.execute(sql, (tarefa.descricao, data_inicio, data_termino, tarefa.status_tarefa))

            self.conexao.commit()

        except Exception as error:
            print(f"Erro ao inserir a tarefa: Erro: `{error}")

    def marcar_concluida(self, descricao):
        try:
            sql = "UPDATE tarefas SET status_tarefa = %s WHERE descricao = %s"
            self.cursor.execute(sql, ("Concluída", descricao))
            self.conexao.commit()
            messagebox.showinfo("Aviso", "Tarefa marcada como concluída.")
        except Exception as error:
            print(f"Erro ao marcar a tarefa como concluída: {error}")

    def excluir_tarefa(self, descricao: str):
        try:
            sql = "DELETE FROM tarefas WHERE descricao = %s"
            self.cursor.execute(sql, (descricao,))
            self.conexao.commit()
        except Exception as erro:
            print(f"Erro ao deletar a tarefa: Erro: {erro}")



