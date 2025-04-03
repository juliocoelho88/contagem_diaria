from tkinter import messagebox, Toplevel, Text, ttk
from tkinter.simpledialog import askinteger
from tkinter.ttk import Button

from tkcalendar import Calendar
from datetime import datetime
from database.db_operations import consultar_dados, inserir_dados, alterar_registro, deletar_registro, exportar_para_excel

def abrir_calendario(data_var):
    """
    Abre um calendário para selecionar uma data.
    """
    def definir_data():
        data_var.set(calendario.get_date())
        janela_calendario.destroy()

    janela_calendario = Toplevel()
    janela_calendario.title("Selecionar Data")
    calendario = Calendar(janela_calendario, date_pattern="yyyy-mm-dd")
    calendario.pack()
    Button(janela_calendario, text="Confirmar", command=definir_data).pack()

def salvar_ou_editar(is_editing, registro_id=None, pelotao_entry=None, data_entry=None, entry_fields=None):
    """
    Salva ou edita um registro no banco de dados.
    """
    pelotao = pelotao_entry.get().strip().upper()
    data = data_entry.get()
    try:
        data = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Erro", "Data inválida!")
        return

    valores = [entry.get() for entry in entry_fields.values()]
    if not pelotao or not data or not valores[0]:
        messagebox.showerror("Erro", "Preencha os campos obrigatórios!")
        return

    try:
        if is_editing and registro_id:
            colunas = ["pelotao", "data"] + list(entry_fields.keys())
            for coluna, valor in zip(colunas, [pelotao, data] + valores):
                alterar_registro(registro_id, coluna, valor)
            messagebox.showinfo("Sucesso", f"Registro com ID {registro_id} atualizado com sucesso!")
        else:
            inserir_dados(pelotao, data, *valores)
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    except Exception as e:
        operation = "editar" if is_editing else "salvar"
        messagebox.showerror("Erro", f"Erro ao {operation} os dados: {e}")

def consultar(janela):
    """
    Exibe os dados da tabela em uma janela.
    """
    resultados = consultar_dados()
    if not resultados:
        messagebox.showinfo("Consulta", "Nenhum registro encontrado.")
        return

    janela_consulta = Toplevel(janela)
    janela_consulta.title("Consulta de Dados")
    tree = ttk.Treeview(janela_consulta, columns=[
        "ID", "Pelotao", "Data", "Pessoa", "Carros", "Motos", "Qnt Ocorrencias",
        "Flagrantes", "Autuacoes", "Raia", "Procurado", "Carro Apreendido",
        "Moto Apreendida", "Flagrantes Outros", "Arma", "Escolas"
    ], show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    for row in resultados:
        tree.insert("", "end", values=row)


def deletar():
    """
    Deleta um registro pelo ID.
    """
    registro_id = askinteger("Deletar Registro", "Digite o ID do registro a ser deletado:")

    # Verifica se um ID foi fornecido
    if not registro_id:
        messagebox.showwarning("Aviso", "Nenhum ID fornecido.")
        return

    try:
        # Chamando a função de deletar registro e verificando o retorno
        resultado = deletar_registro(registro_id)
        if resultado:
            messagebox.showinfo("Sucesso", f"Registro com ID {registro_id} deletado com sucesso!")
        else:
            # Se nenhum registro foi afetado, isso significa que o ID não existe
            messagebox.showerror("Erro", f"Nenhum registro encontrado com ID {registro_id}.")
    except Exception as e:
        # Caso haja um erro inesperado, exiba a mensagem
        messagebox.showerror("Erro", f"Erro ao tentar deletar registro: {e}")


def exportar():
    """
    Exporta os dados para um arquivo Excel.
    """
    try:
        nome_arquivo = "contagem_diaria_export.xlsx"
        exportar_para_excel(nome_arquivo)
        messagebox.showinfo("Sucesso", f"Dados exportados para {nome_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar os dados: {e}")

def editar(pelotao_entry, data_entry, entry_fields, salvar_button, registro_id_var):
    # Solicitar o ID do registro a ser editado
    registro_id = askinteger("Editar Registro", "Digite o ID do registro:")
    if not registro_id:
        return

    # Consultar os dados do registro com o ID fornecido
    resultados = consultar_dados(f"id = {registro_id}")
    if not resultados:
        messagebox.showerror("Erro", f"Nenhum registro encontrado com ID {registro_id}.")
        return

    # Preencher os campos com os dados do registro
    registro = resultados[0]
    pelotao_entry.set(registro[1])
    data_entry.delete(0, "end")
    data_entry.insert(0, registro[2])  # Supondo que a data está na posição 2

    for idx, campo in enumerate(entry_fields.keys(), start=3):
        entry_fields[campo].delete(0, "end")
        entry_fields[campo].insert(0, registro[idx])

    # Alterar o botão "Salvar" para "Salvar Alterações"
    salvar_button.config(
        text="Salvar Alterações",
        command=lambda: salvar_ou_editar(
            is_editing=True,
            registro_id=registro_id,
            pelotao_entry=pelotao_entry,
            data_entry=data_entry,
            entry_fields=entry_fields
        )
    )

def limpar_campos(pelotao_entry, data_entry, entry_fields):
    """
    Limpa todos os campos de entrada da interface.
    """
    if hasattr(pelotao_entry, "set"):  # Se for um Combobox com StringVar
        pelotao_entry.set("")
    else:  # Se for um Entry
        pelotao_entry.delete(0, "end")

    if hasattr(data_entry, "set"):  # Se for uma StringVar
        data_entry.set("")
    else:  # Se for um Entry
        data_entry.delete(0, "end")

    for entry in entry_fields.values():
        entry.delete(0, "end")
