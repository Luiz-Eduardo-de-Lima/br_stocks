import pandas as pd
from zipfile import ZipFile
import plotly.express as px
import wget
import os

def get_statements(begin = int, end = int):
    '''
    Retorna TODOS os balanços de TOTAS empresas de capital aberto disponíveis na CVM desde 2011.
    '''
    base_url = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/'
    try:
        os.system(f'rm -fr statements')
    except:
        pass

    for year in range(begin, end +1):
        wget.download(base_url + f'itr_cia_aberta_{year}.zip')

        with ZipFile(f'itr_cia_aberta_{year}.zip', 'r') as zip:
            zip.extractall('statements')
            os.system(f'rm -fr itr_cia_aberta_{year}.zip')
        
    statements = ['BPA','BPP','DFC_MD','DFC_MI','DMPL','DRA','DRE','DVA']
    statements_type = ['ind', 'con']

    for stt in statements:

        for stt_tp in statements_type:
            data = pd.DataFrame()

            for year in range(begin, end +1):
                input_stt = pd.read_csv(
                    f'statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv',
                    sep = ';',
                    decimal = ',',
                    encoding='ISO-8859-1')
                data = pd.concat([data, input_stt])
                os.system(f'rm -fr statements/itr_cia_aberta_{stt}_{stt_tp}_{year}.csv')
                
            data.to_csv(f'statements/{stt}_{stt_tp}_from_{begin}_to_{end}.csv', index = False)
    return

def get_ebit(company = str,begin = int, end = int):
    try:
        data = pd.read_csv(
            f'statements/DRE_ind_from_{begin}_to_{end}.csv',
            sep = ',',
            encoding = 'UTF-8'
            )
    except:
        print('Baixe os demonstrativos para executar essa função.')

    data = pd.DataFrame(data)[['DENOM_CIA', 'ORDEM_EXERC', 'DT_INI_EXERC', 'DT_FIM_EXERC', 'CD_CONTA', 'DS_CONTA', 'VL_CONTA']]
    data['DT_INI_EXERC'] = pd.to_datetime(data['DT_INI_EXERC'], format = '%Y-%m-%d')
    data['DT_FIM_EXERC'] = pd.to_datetime(data['DT_FIM_EXERC'], format = '%Y-%m-%d')

    dre_company = data[data['DENOM_CIA'] == company][data['ORDEM_EXERC'] == 'ÚLTIMO']
    
    ebit = pd.DataFrame(
        dre_company[dre_company['CD_CONTA'] == 'Resultado Antes dos Tributos sobre o Lucro'][['DT_FIM_EXERC','DS_CONTA','VL_CONTA']]
        )
    return ebit