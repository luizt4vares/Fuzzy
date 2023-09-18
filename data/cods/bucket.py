import logging 
import pandas as pd
from data.cods.normalization import process as NormProcess

class BucketMainProcess():
    def __init__(self,df,
                 lista_meds_df,
                 lista_count_df,name) -> None: 
        self.name=name
        self.response = self.bucket_main_process(df)

        if str(type(self.response)) == "<class 'pandas.core.frame.DataFrame'>":
            self.response['meds']=lista_meds_df
            self.response['buckt_meds'] = self.response['buckt'].astype(str) + pd.Series(map(str, lista_count_df))
            self.response['Item Title New'] = self.response['Item Title'].apply(lambda x: NormProcess(x))
            self.response.to_csv(f"../fuzzy_string/data/base_processada/{self.name}_process.csv",encoding="utf-8-sig")

    def get_response(self):
        return self.response
    
    def bucket_create(self,dados:list) -> list:
        def price_check(val:int) -> str:
            if val <10:
                return "<10"
            elif val <20:
                return "<20"
            elif val<40:
                return "<40"
            elif val<80:
                return "<80"
            elif val<100:
                return '<100'
            elif val<200:
                return "<200"
            elif val<300:
                return "<300"
            elif val >=300:
                return ">=300"
            
        lista = [price_check(x) for x in dados]
        return lista
    


    def bucket_main_process(self,df):
        # criando coluna com bucket
        logging.info('[main] -> Gerando buckt nos DFs')
        try:
            logging.info('          -> Gerando buckt no df competidor')
            df['buckt'] = self.bucket_create(df['Promo Price'].to_list())
        except Exception as error:
            logging.error(f'''[Main] - > Erro ao gerar buckt no df {self.name} (
            >>> {error}
            )''')
            return False

        return df         
