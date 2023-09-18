import logging 
from data.cods.utils import *
import pandas as pd

def processando_dados(competidor_path:str = "data/base/meliitenss.csv",
         shopee_path:str = 'data/base/shopeeitens.csv',
         buckt_tup =("<10","<20","<40","<80",'<100',"<200","<300",">=300")
        ):

    
    # lendo dfs
    logging.info("================== Inicio Processo ==================")
    logging.info("[Main] -> Lendo bases...")
    try:
        competidor_df = pd.read_csv(competidor_path)
        shopee_df = pd.read_csv(shopee_path)
    except Exception as error:
        logging.error(f'''[Main] -> Erro ao ler base (
        >>> {error}
        )''')
        return

    if type(base_comp_process(competidor_df))==bool:
        return False

    if type(base_shopee_process(shopee_df))==bool:
        return False
