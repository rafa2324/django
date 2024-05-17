import os
import pandas as pd
import base.config as PARAMS
from base.libs.app import columns_str_to_type
from base.libs.sheet import Sheet
import openpyxl


class ExcelPd():
    filepath = str
    error_code = int
    aError_message = []
    aSheet = []
    oSheet = Sheet
    #----
    df = []
    found = bool
    rows = int
    columns = int

           
    def __init__(self, filepath):
        self.filepath = filepath
    
    def file_exist(self):
        return os.path.exists(self.filepath)

    def get_sheet(self, sheet_name, columns_dtype=None):
        '''
            Retorna un objeto Sheet con datos del sheet leido.
            
            Parameters:
                sheet_name : nombre del sheet a leer del archivo self.filepath
                columns_dtype : dict dtype. dtype={'col1':str,'col2':str,...}
            
            Return:
                True or False
                Los datos se guardan en self.oSheet 
                Los mensajes se guardan en aError_message 
        '''
        print(sheet_name)
        if columns_dtype == None:
            columns_dtype = {}
        self.oSheet = Sheet()
        self.oSheet.sheet_name = sheet_name
        self.oSheet.df = []
        self.oSheet.rows = 0
        self.oSheet.columns = 0
        self.oSheet.is_found = False
        try:
            self.oSheet.df = pd.read_excel(open(self.filepath, 'rb'),
                                    sheet_name=sheet_name,
                                    dtype=columns_dtype,
                                    na_values='')
            self.oSheet.df = self.oSheet.df.fillna('')
            self.oSheet.rows, self.oSheet.columns = self.oSheet.df.shape
            self.oSheet.is_found = True
            # self.aError_message.append(PARAMS.Messages.found)
        except Exception as e:
            self.error_code = PARAMS.ErrorCode.exception
            self.aError_message.append(e)

        return True if self.oSheet.is_found else False

    def get_sheets(self, aSheet_name):
        '''
            Lee una relacion de sheets y las almacena en aSheet (lista de Sheet)
            
            Parameters:
                aSheet_name : una lista  de diccionarios que contiene los sheet_name
                            a leer. [{ 'sheet_name': str, 'columns_dtype':dict dtype },...]
            
            Return:
                True or False si se encontró un error.
        '''
        self.aSheet = []
        ok = True
        for sheet in aSheet_name:
            print('gardos', sheet['sheet_name'], sheet['columns_dtype'])
            if self.get_sheet(sheet['sheet_name'], sheet['columns_dtype']):
                print(self.oSheet.is_found, self.oSheet.df)
                self.aSheet.append(self.oSheet)
            # else:
            #     ok = False
        return ok
          
        
    # REVISAR PARA ELIMINAR
        
    def get_document(self):
        self.df = []
        self.found = False
        self.error_message = PARAMS.Messages.not_found
        try :
            #self.filepath = pd.ExcelFile(self.filepath, engine='openpyxl')
            self.df = pd.read_excel(open(self.filepath, 'rb'))
            self.rows, self.columns = self.df.shape
            self.found = True
            self.error_message = PARAMS.Messages.found
        except:
            pass
        
        return self.df
    
    def load_excel_config(self):
        ''' 
            Lee de self.filepath el sheet con nombre PARAMS.SHEET_NAME_CATALOGOS
            que contiene una relación de nombre de catálogos.
            Luego por cada item lee de self.filepath un sheet con nombre item.catalog_name 
            y lo adiciona en self.aSheet 
            Pre Validate:
                verifica que archivo self.filepath exista
                verifica que exista sheet llamado PARAMS.SHEET_NAME_CATALOGOS
            Return:
                True : si la carga es ok
                False : si ocurrió un error => self.error_code, self.error_message
        '''
        self.error_code = PARAMS.ErrorCode.ok
        self.error_message = ''
        self.aSheet = []
        
        # if not self.file_exist():
        #     self.error_code = PARAMS.ErrorCode.not_found
        #     self.error_message = PARAMS.Messages.excel_catalogos_not_found
        #     return False
        
        # self.get_sheet(PARAMS.SHEET_NAME_CATALOGOS)
        # if not self.found:
        #     self.error_code = PARAMS.ErrorCode.data_error
        #     self.error_message = PARAMS.Messages.excel_catalogos_data_error
        #     return False
        # # append sheet __catalogos__
        # self.aSheet.append({
        #         'catalog_name' : PARAMS.SHEET_NAME_CATALOGOS,
        #         'found' : self.found,
        #         'df' : self.df
        #     })
        # # append sheets segun filas del sheet __catalogos__       
        # for _, row in self.df.iterrows(): 
        #     catalog_name = row['catalog_name']
        #     columns_type = columns_str_to_type(row['columns_str'])
            
        #     df = self.get_sheet(sheet_name=catalog_name, columns_type=columns_type)
        #     self.aSheet.append({
        #         'catalog_name' : catalog_name,
        #         'found' : self.found,
        #         'df' : df
        #     })
        
        return True
          
    def load_excel_catalogs(self, aCatalogCab):
        '''
            Adiciona en self.aSheet datos de los sheets leidos de self.filepath para cada
            item de aCatalogCab. El sheet name viene dado en aCatalogCab.sheet_name.
            
            Parameters:
                aCatalogCab : es una lista de dict de tipo Catalogo.aSheet
            
            Pre validate:
                self.filepath exista
            
            Return:
                True : Carga ok
                False : Ocurrió un error => self.error_code, self.error_message
        '''
        if not self.file_exist():
            self.error_code = PARAMS.ErrorCode.not_found
            self.error_message = PARAMS.Messages.excel_catalogos_not_found
            return False
        
        self.aSheet = []
        # print(self.filepath)
        # for catalog in aCatalogCab:
        #     print(catalog.sheet_name, catalog.columns_type)
        #     df = self.get_sheet(catalog.sheet_name, catalog.columns_type)
        #     catalog.found = self.found  
        #     catalog.state = f'{self.rows} registros.'
        #     self.aSheet.append({
        #             'catalog_name' : catalog.catalog_name,
        #             'found' : self.found,
        #             'df' : self.df
        #     })
        return True