import logging 
from data.cods.process_dados import processando_dados
from data.cods.fuzz import fuzzyMain
import warnings
import sys
from data.cods.normalization import process as NormProcess

# Defina o encoding ao imprimir
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(filename='data/log_base/log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M')
# Ignorar todos os avisos
warnings.filterwarnings("ignore")



if __name__ == "__main__":
    processando_dados()
    fuzzyMain()
    

