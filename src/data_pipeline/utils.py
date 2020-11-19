"""!@brief Utility collection for the pipeline process.
@file Data pipeline utility file.
@author Martin Schuck
@date 11.8.2020
"""


from collections import namedtuple


med_codes = ['EVT', 'SHL', 'BAS', 'BAYN', 'FMS', 'FRE.DE', 'JNJ', 'PFE', 'ABT',
             'KMB', 'MDT', 'PHG', 'GE', 'BDX', 'CAH', 'SYK']
bank_codes = ['DB', 'ICK', 'GS', 'CMC', 'BRYN', 'NCB', 'WFC', 'JPHLF', 'CICHY',
              'ACGBY', 'CRARY', 'BACHF', 'C']
energy_codes = ['SIEGY', 'EOAN.DE', 'RWE.DE', 'DUK', 'ENGI.PA', 'NGG', 'NEE',
                'EDF']
oil_codes = ['CVX', 'XOM', 'PTR', 'RDS-A', 'LUK', 'ROSN', 'TOT', 'BP', 'SNP']
steel_codes = ['TKA.DE', 'MT', 'NISTF', 'SHE:000709', 'SHA:600019', 'PKX', 'SHE:002075']
automotive_codes = ['TM', 'GM', 'HYMTF', 'BMW.DE', 'NSU', 'VOW.DE', 'DAI.DE',
                    'CON', 'TSLA']
telecom_codes = ['DTE', 'DRI', 'TEF', 'O2D.DE', 'T', 'TMUS', 'VOD', 'CTM', 'VZ',
                 'NTT.F', 'SFTBY', 'AMOV', 'CHA']
tech_codes = ['AAPL', 'AMZN', 'GOOGL', 'CCCMF', 'IFX.DE', 'SAP', 'CSCO', 'IBM',
              'INL', 'INTC', 'MSF', 'EBAY', 'EA', 'TWTR', 'QCOM', 'SNE', 'TXN',
              'NFC', 'ZM']

Domain = namedtuple('domain', ['df_column_name', 'stock_code_list'])
sector_tuple_list = [Domain('stock_med', med_codes), Domain('stock_bank', bank_codes),
                     Domain('stock_energy', energy_codes),
                     Domain('stock_oil', oil_codes), Domain('stock_steel', steel_codes),
                     Domain('stock_automotive', automotive_codes),
                     Domain('stock_telecom', telecom_codes), Domain('stock_tech', tech_codes)]

index_codes = ['DAX', 'NDAQ']
