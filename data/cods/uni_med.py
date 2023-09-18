from functools import lru_cache
import nltk
from tqdm import tqdm
class UnidadeMedida():
    def __init__(self,lista_medidas:list,base) -> None:
        self.dic_med:dict={"Names":{
        "ram":"Memoria","mega":"Memoria","bts":"Memoria",
        "gb":"Espaco","tb":"Espaco","kb":"Espaco","bt":"Espaco","mb":"Espaco",
        "l":"Vol","litro":"Vol","ml":"Vol","Ltrs":"Vol","litros":"Vol",
        "tonelada":"Peso","kg":"Peso","grama":"Peso","gr":"Peso","kilo":"Peso","quilo":"Peso","lb":"Peso","mg":"Peso","g":"Peso","t":"Peso","libros":"Peso",
        "w":"Eletrico","v":"Eletrico","kw":"Eletrico","wts":"Eletrico","watts":"Eletrico","volts":"Eletrico","kwh":"Eletrico",
        "un":"Quant","unidade":"Quant","uni":"Quant","kit":"Quant","volume":"Quant","vol":"Quant","unid":"Quant","pcts":"Quant","pares":'Quant',
        "km":"Medida","mm":"Medida","m":"Medida","polegadas":"Medida","cm":"Medida","metros":"Medida","centimetro":"Medida","ft":"Medida","largura":"Medida","altura":"Medida","Metros":"Medida"
        },"data":{
        "Memoria": 0.3,
        "Espaco": 0.5,
        "Vol":1,
        "Peso":0.9,
        "Eletrico":0.2,
        "Quant":0.9,
        "Medida":0.5
        }
        } 

        self.list_ret=[]

        for lista_meds_name in tqdm(lista_medidas, desc=f"Processando {base}"):
            l=[]
            for lista_meds_word in lista_meds_name:
                [l.append({med:[nltk.edit_distance(lista_meds_word[1],med),lista_meds_word]}) if nltk.edit_distance(lista_meds_word,med)<=1 else None for med in self.dic_med["Names"]]

            if len(l)>0:
                results = self.get_lower_lev_dist(l)
                final=[]
                [final.append([self.dic_med['data'][self.dic_med['Names'][result[0]]],result[1]]) for result in results]
                if len(final)==0:
                    self.list_ret.append(None)
                else:
                    self.list_ret.append(final)
            else:
                self.list_ret.append(None)
    def response(self) -> list:
        return self.list_ret,[0 if val==None else len(val) for val in self.list_ret]
    
    def return_med(self,s1,s2,f=False):
        if self.lev_dist(s1,s2) == 0:
            if f==True:
                return self.lev_dist(s1,s2)
            return True
        else:
            return False
        
    def get_lower_lev_dist(self,valores:list):
        result=[]
        i=0
        for val in valores:
            [result.append([key,val[key][1]]) if val[key][0] == 0 else None for key in val]
            i+=1
        return result
    
    # retorna distancia de uma palavra para outra
    def lev_dist(self,a, b):
        @lru_cache(None)  # for memorization
        def min_dist(s1, s2):
            if s1 == len(a) or s2 == len(b):
                return len(a) - s1 + len(b) - s2

            # no change required
            if a[s1] == b[s2]:
                return min_dist(s1 + 1, s2 + 1)

            return 1 + min(
                min_dist(s1, s2 + 1),      # insert character
                min_dist(s1 + 1, s2),      # delete character
                min_dist(s1 + 1, s2 + 1),  # replace character
            )

        return min_dist(0, 0)