from database.db_config import criar_tabela
from interface.ui_main import iniciar_interface
import logging
import sys

# Configuração do log
LOG_FILE = "app_error.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Redirecionar erros para o log
def excecao_capturada(exc_type, exc_value, exc_traceback):
    logging.error("Erro capturado", exc_info=(exc_type, exc_value, exc_traceback))
    print("Ocorreu um erro! Veja o arquivo app_error.log para mais detalhes.")

sys.excepthook = excecao_capturada


def main():
    criar_tabela()
    iniciar_interface()

if __name__ == "__main__":
    main()
