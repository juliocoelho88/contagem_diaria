from tkinter import Tk, StringVar, Entry
from tkinter.ttk import Combobox, Button, Labelframe, Label
from interface.ui_helpers import salvar_ou_editar, consultar, deletar, exportar, abrir_calendario, editar


def iniciar_interface():
    """
    Inicializa a interface principal da aplicação.
    """
    janela = Tk()
    janela.title("Cadastro de Contagem Diária")
    janela.geometry("900x700")

    registro_id_var = StringVar()  # Variável para armazenar o ID do registro em edição

    # Frame: Informações Básicas
    frame_info = Labelframe(janela, text="Informações Básicas")
    frame_info.pack(fill="x", padx=10, pady=10)

    Label(frame_info, text="Pelotão:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    pelotao_var = StringVar()
    pelotao_entry = Combobox(frame_info, textvariable=pelotao_var, values=["A", "B", "C", "D", "RPMA", "RPMC", "REM", "REV"])
    pelotao_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    Label(frame_info, text="Data:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    data_var = StringVar()
    data_entry = Entry(frame_info, textvariable=data_var)
    data_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    Button(frame_info, text="Selecionar Data", command=lambda: abrir_calendario(data_var)).grid(row=1, column=2, padx=10, pady=5)

    # Frame: Dados de Entrada
    frame_dados = Labelframe(janela, text="Dados de Entrada")
    frame_dados.pack(fill="x", padx=10, pady=10)

    entry_labels = [
        "Pessoa", "Carros", "Motos", "Qnt_Ocorrencias", "Flagrantes",
        "Autuacoes", "RAIA", "Procurado", "Carro_Apreendido",
        "Moto_Apreendido", "Flagrantes_Outros", "Arma"
    ]
    entry_fields = {}

    for idx, label in enumerate(entry_labels):
        Label(frame_dados, text=f"{label}:").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry = Entry(frame_dados)
        entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
        entry_fields[label] = entry

    # Frame: Ações
    frame_acoes = Labelframe(janela, text="Ações")
    frame_acoes.pack(fill="x", padx=10, pady=10)

    salvar_button = Button(
        frame_acoes,
        text="Salvar",
        command=lambda: salvar_ou_editar(
            is_editing=False,
            pelotao_entry=pelotao_entry,
            data_entry=data_entry,
            entry_fields=entry_fields
        )
    )
    salvar_button.grid(row=0, column=0, padx=10, pady=10)

    Button(
        frame_acoes,
        text="Consultar",
        command=lambda: consultar(janela)
    ).grid(row=0, column=1, padx=10, pady=10)

    Button(
        frame_acoes,
        text="Editar",
        command=lambda: editar(
            pelotao_entry=pelotao_entry,
            data_entry=data_entry,
            entry_fields=entry_fields,
            salvar_button=salvar_button,
            registro_id_var=registro_id_var
        )
    ).grid(row=0, column=2, padx=10, pady=10)

    Button(
        frame_acoes,
        text="Deletar",
        command=deletar
    ).grid(row=0, column=3, padx=10, pady=10)

    Button(
        frame_acoes,
        text="Exportar",
        command=exportar
    ).grid(row=0, column=4, padx=10, pady=10)

    janela.mainloop()
