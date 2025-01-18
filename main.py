from database.db_config import criar_tabela
from interface.ui_main import iniciar_interface

def main():
    criar_tabela()
    iniciar_interface()

if __name__ == "__main__":
    main()
