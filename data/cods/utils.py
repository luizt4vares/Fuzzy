import logging
import re
from data.cods.uni_med import UnidadeMedida as UMed
from data.cods.bucket import BucketMainProcess as BucMainProcs

def base_comp_process(competidor_df):
    # Obtenha uma lista de todas as unidades disponíveis
    logging.info('[main] -> Gerando listas com unidades de medida Base_S2')
    try:
        lista_meds_comp,count_meds_comp = UMed([re.findall(r'(\d+)\s*(\w+)', str(nomes).lower()) for nomes in competidor_df['Item Title'].tolist()],"Base_S2").response()
    except Exception as error:
        logging.error(f'''[Main] - > Erro ao gerar lista com unidade de medidas Base_S2(
        >>> {error}
        )''')
        return False
    # gerando bucket
    response_buckt_comp = BucMainProcs(competidor_df,lista_meds_comp,count_meds_comp,"Base_S2").get_response()
    if type(response_buckt_comp)==bool:
        return False
    
def base_shopee_process(shopee_df):
    logging.info('[main] -> Gerando listas com unidades de medida Base_S1')
    try:
        lista_meds_shopee,count_meds_shopee = UMed([re.findall(r'(\d+)\s*(\w+)', str(nomes).lower()) for nomes in shopee_df['Item Title'].tolist()],"Base_S1").response()
    except Exception as error:
        logging.error(f'''[Main] - > Erro ao gerar lista com unidade de medidas Base_S1(
        >>> {error}
        )''')
        return False
    # gerando bucket
    response_buckt_shopee = BucMainProcs(shopee_df,lista_meds_shopee,count_meds_shopee,"Base_S1").get_response()
    if type(response_buckt_shopee)==bool:
        return False