import logging 
import csv
import ast
import pandas as pd
from fuzzywuzzy import fuzz
import re
import time
from tqdm import tqdm
class fuzzyMain():
    def __init__(self,
                Base_S1="data/base_processada/Shopee_process.csv",
                Base_S2="data/base_processada/competidor_process.csv"
                ) -> None:
        self.comp_path=Base_S1
        self.shopee_path=Base_S2
        self.write_csv(['Shop ID','Shopname','Meli id','Item Title','Promo Price','Link','L1 Category','buckt','meds',	
                                             'buckt_meds','score','score_medida','Item ID shopee',	'Item Title shopee',	
                                             'Shop ID shopee',	'Shopname shopee',	
                                             'L1 Category shopee',	'item_price shopee',	
                                             'price shopee','Promo Price shopee','link shopee'])
        shopee_df = pd.read_csv(self.shopee_path,encoding="utf-8-sig")
        comp_df=pd.read_csv(self.comp_path,encoding="utf-8-sig")

        # [self.df_return.to_csv("../fuzzy_string/df_retorno.csv",encoding="utf-8-sig") if self.get_val(_df_,comp_df,i)==True else None for i,_df_ in shopee_df.iterrows()]
        [self.save_retorno() if self.get_val(_df_,comp_df,i)==True else None for i,_df_ in tqdm(shopee_df.iterrows(), total=len(shopee_df))]
    
    def write_csv(self,lista):
        with open('df_retorno.csv', 'a',encoding="utf-8-sig", newline='') as f:
            write = csv.writer(f)
            write.writerow(lista)
    def save_retorno(self):
        [self.write_csv(row.tolist()) for i,row in self.df_return.iterrows()]
        pass
    def calculate_similarity(self,row,_df_name):
        title_clean = re.sub(r'[^A-Za-z0-9\s]', '', row['Item Title New'])
        return fuzz.token_sort_ratio(_df_name,title_clean)
    
    def get_val(self,_df_,comp_df,i,metrica_score = 80,metrica_score_medida=80):
        logging.info(f'================ {i} ================')
        start = time.perf_counter()
        self.df_return = pd.DataFrame()
        # primeiro vamos puxar o df competidor filtrado
        comp_df_filt = comp_df.loc[comp_df['buckt_meds']==_df_['buckt_meds']]

        # se não acharmos nd do mesmo bucket iremos retornar None para o item
        if type(comp_df_filt)=='NoneType' or comp_df_filt.shape[0]==0:
            return False
        
        start2 = time.perf_counter()
        # com ou sem unidade de medida já podemos tirar o score
        comp_df_filt['score'] = comp_df_filt.apply(lambda x: self.calculate_similarity(x,_df_['Item Title New']), axis=1)
        maior_score = comp_df_filt['score'].max(axis=0)
        # filtrando score
        comp_df_filt = comp_df_filt[['Shop ID', 'Shopname', 'Meli id', 'Item Title','Promo Price', 'Link', 'L1 Category', 'buckt', 'meds', 'buckt_meds','score']].loc[comp_df_filt['score']>=metrica_score]
        logging.info(f"tempo para tirar score dos itens {time.perf_counter()-start2}")
        # if para garantir que achamos algo no filtro
        if not comp_df_filt.shape[0] == 0:
            # processo sem analise de medida
            if int(_df_['buckt_meds'][-1])==0:
                comp_df_filt['score_medida']=""
                self.save_df(comp_df_filt,_df_)
                logging.info(f"tempo para salvar os dados localizados {time.perf_counter()-start}")
                return True
            # processo com medida
            else:
                lista=[]
                for idn,_df_comp in comp_df_filt.iterrows():
                    lista.append(self.get_score_metrica(_df_,_df_comp))
                comp_df_filt['score_medida']=lista
                comp_df_filt=comp_df_filt.loc[comp_df_filt['score_medida']>metrica_score_medida]
                self.save_df(comp_df_filt,_df_)
                return True
        else:
            logging.info(f"nn achou, maior score ->  {maior_score} buckt -> {_df_['buckt']} ")
            return False

    def get_score_metrica(self,_df_shopee,_df_comp):
        igual=0
        meds=ast.literal_eval(_df_shopee['meds'])
        meds_comp=ast.literal_eval(_df_comp['meds'])
        for med in meds:
            for med_comp in meds_comp:
                if med[1][1] == med_comp[1][1] and med[1][0] == med_comp[1][0]:
                    igual+=1
        if len(meds)<len(meds_comp):
            score_metrica = igual/len(meds)
        else:
            score_metrica = igual/len(meds_comp)
        return score_metrica*100
    

    def save_df(self,comp_df_filt,_df_):
        comp_df_filt[['Item ID shopee','Item Title shopee', 'Shop ID shopee', 'Shopname shopee', 'L1 Category shopee', 'item_price shopee', 'price shopee', 'Promo Price shopee', 'link shopee']] = \
        _df_[['Item ID','Item Title', 'Shop ID', 'Shopname', 'L1 Category', 'item_price', 'price', 'Promo Price', 'link']].tolist()
        self.df_return=pd.concat([self.df_return,comp_df_filt.reset_index(drop=True)])