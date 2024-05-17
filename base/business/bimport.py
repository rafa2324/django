from datetime import datetime
import pandas as pd

from .bcainvdet import BCaInvDet

from ..models import Producto
from .bunidadmedida import BUnidadMedida
from base.libs.excelpd import ExcelPd
import numpy as np
from base.config import ImportSheet
from base.business.bproducto import BProducto
from base.business.bstock import BStock


class BImport():
    request = None
    aMessage = []
    aSheet = {
        ImportSheet.producto: {
            'sheet_name' : 'PRODUCTOS',
            'aColumn': {
                's_codigo': 0,
                'unidad_medida_s_codigo': 1,
                's_descripcion': 2,
                's_categoria': 3
            },
            'oSheet': None
        },
        ImportSheet.stock: {
            'sheet_name' : 'STOCK',
            'aColumn': {
                's_codigo': 1,
                's_ubicacion': 4,
                'n_stk_act': 5,
            },
            'oSheet': None
        },
    }
    
    def __init__(self, request):
        self.request = request

    def getExcel(self, filename):
        '''
            Lee los sheet y actualiza el self.aSheet[x]['df'] correspondiente
            
            Parameters:
                filenane : url del excel a leer
            
            Return:
                True si leyo correctamente todos los sheet, False caso contrario
        '''
        ok = False
        oExcelPd = ExcelPd(filename)
        # lee sheet producto
        if not oExcelPd.get_sheet(self.aSheet[ImportSheet.producto]['sheet_name']):
            self.aMessage += oExcelPd.aError_message
        else:
            self.aSheet[ImportSheet.producto]['oSheet'] = oExcelPd.oSheet
            ok = True
        
        # lee sheet stock
        if not oExcelPd.get_sheet(self.aSheet[ImportSheet.stock]['sheet_name']):
            ok = False
            self.aMessage += oExcelPd.aError_message
        else:
            self.aSheet[ImportSheet.stock]['oSheet'] = oExcelPd.oSheet
            
        return ok

    def import_unidad_medida(self):
        ok = False

        # obtener df productos
        df_producto:pd.DataFrame = self.aSheet[ImportSheet.producto]['oSheet'].df
        
        if df_producto.empty:
            self.aMessage.append(f'No hay datos en hoja {self.aSheet[ImportSheet.producto]["sheet_name"]}')
            return ok
        
        # crear nuevo df con columna unidades de df_producto
        df_unidades = pd.DataFrame()
        df_unidades['unidad'] = df_producto.iloc[:,
                        self.aSheet[ImportSheet.producto]['aColumn']['unidad_medida_s_codigo']]
                
        # agrupar df_unidades por columna unidad (una unica fila pñor unidad)
        # groupby devuelve type obj Serie, pero con el reset_ibdex retornaun DF
        # reset_index agrega un indice y mueve las columnas
        df_unidades_group = df_unidades.groupby('unidad').size().reset_index()

        # reemplazar los valores en blanco por nan
        df_unidades_group['unidad'].replace('', np.nan, inplace=True)
                
        # eliminar filas que contengan valores nan
        df_unidades_group = df_unidades_group.dropna()
                
        # rename columnas 
        # la 1era columna paso a ser 'unidad', luego del reset_index)
        # la columna con el count es 0                
        df_unidades_group = df_unidades_group.rename(columns={0:'count'})

        # recorrer df_unidades_group e insertar en modelo UNidadMedida
        # si no existe
        oBUnidadMedida = BUnidadMedida()
        count = 0
        ok = True
        for _, row in df_unidades_group.iterrows():
            producto = oBUnidadMedida.get_by_s_codigo(row['unidad'].strip())
            if producto == None:
                if oBUnidadMedida.save(self.request, 'new', 0, {
                    's_codigo':row['unidad'].strip(),
                    's_descripcion':row['unidad'].strip(),
                    'user_id': 1,
                    'license_id': 1
                }):
                    count +=1
                else:
                    ok = False
                    self.aMessage.append(oBUnidadMedida.message)

            #print('row', row['unidad'], row['count'])
        self.aMessage.append(f'UnidadMedida: insertados {count} de {df_unidades_group.shape[0]}')

        return ok
    
    def importar_producto(self):
        ok = False

        # obtener df productos
        df_producto:pd.DataFrame = self.aSheet[ImportSheet.producto]['oSheet'].df

        df_producto = df_producto.rename(columns={
            df_producto.columns[self.aSheet[ImportSheet.producto]['aColumn']['s_codigo']]:'s_codigo', 
            df_producto.columns[self.aSheet[ImportSheet.producto]['aColumn']['unidad_medida_s_codigo']]:'unidad_medida_s_codigo', 
            df_producto.columns[self.aSheet[ImportSheet.producto]['aColumn']['s_descripcion']]:'s_descripcion',
            df_producto.columns[self.aSheet[ImportSheet.producto]['aColumn']['s_categoria']]:'s_categoria'
            })
        
        # elimina filas con descripcion en blanco
        df_producto['s_descripcion'].replace('', np.nan, inplace=True)
        df_producto = df_producto.dropna()

        if df_producto.empty:
            self.aMessage.append(f'No hay datos en hoja {self.aSheet[ImportSheet.producto]["sheet_name"]}')
            return ok
        
        # recorre filas e inserta o actualiza Producto
        count = {
            'insert' : 0,
            'update' : 0,
            'error': 0,
        }
        ok = True
        oBProducto = BProducto()
        oBUnidadMedida = BUnidadMedida() 
        for _, row in df_producto.iterrows():
            s_codigo = row['s_codigo'].strip()
            producto = oBProducto.get_by_s_codigo(s_codigo)
            unidad_medida = oBUnidadMedida.get_by_s_codigo(row['unidad_medida_s_codigo'])
            if unidad_medida == None:
                self.aMessage.append(f"Producto: Error, no se encontró unidad {row['unidad_medida_s_codigo']}")
                count['error'] += 1
                ok = False
            else:
                data = {
                    's_codigo': s_codigo,
                    's_descripcion': row['s_descripcion'][:100],
                    's_categoria': row['s_categoria'],
                    'unidad_medida': unidad_medida,
                    'user_id': 1,
                    'license_id': 1
                }
                error = False
                if producto != None:
                    if not oBProducto.save(self.request, 'edit', producto.id, data, producto):
                        error = True
                    else:
                        count['update'] += 1
                else:
                    if not oBProducto.save(self.request, 'new', 0, data):
                        error = True
                    else:
                        count['insert'] += 1
                if error:
                    self.aMessage.append(oBProducto.message)
                    count['error'] += 1
                

        self.aMessage.append(f'Producto: {count["insert"]} insertados, {count["update"]} actualizados de {self.aSheet[ImportSheet.producto]["oSheet"].rows}')
        return ok

    def import_stock(self):
        ok = False

        # obtener df stock
        df_stock:pd.DataFrame = self.aSheet[ImportSheet.stock]['oSheet'].df
        
        if df_stock.empty:
            self.aMessage.append(f'No hay datos en hoja {self.aSheet[ImportSheet.stock]["sheet_name"]}')
            return ok
        
        # crear nuevo df con columna s_codigo de df_stock
        df_stock_filter = pd.DataFrame()
        df_stock_filter = df_stock.iloc[:, 
                        [
                            self.aSheet[ImportSheet.stock]['aColumn']['s_codigo'],
                            self.aSheet[ImportSheet.stock]['aColumn']['s_ubicacion'],
                            self.aSheet[ImportSheet.stock]['aColumn']['n_stk_act']
                        ]]
        df_stock_filter = df_stock_filter.rename(columns={
                df_stock_filter.columns[0]:'s_codigo',
                df_stock_filter.columns[1]:'s_ubicacion',
                df_stock_filter.columns[2]:'n_stk_act'}
            )
        print(df_stock_filter.head())

        # agrupar df_unidades por columna unidad (una unica fila pñor unidad)
        # groupby devuelve type obj Serie, pero con el reset_ibdex retornaun DF
        # reset_index agrega un indice y mueve las columnas
        df_stock_group = df_stock_filter.groupby('s_codigo')['n_stk_act'].sum().reset_index()

        print('GROUP', df_stock_group.head())

        # reemplazar los valores en blanco por nan
        df_stock_group['s_codigo'].replace('', np.nan, inplace=True)
                
        # eliminar filas que contengan valores nan
        df_stock_group = df_stock_group.dropna()
                
        # rename columnas 
        # la 1era columna paso a ser 'unidad', luego del reset_index)
        # la columna con el count es 0                
        df_stock_group = df_stock_group.rename(columns={0:'sum'})

        print(df_stock_group.head())
        print(f"{df_stock_group.shape[0]} de {df_stock.shape[0]}")

        count = {
            'insert' : 0,
            'update' : 0,
            'error': 0,
        }
        ok = True
        oBProducto = BProducto()
        oBStock = BStock()
        for _, row in df_stock_group.iterrows():
            s_codigo = row['s_codigo'].strip()
            producto = oBProducto.get_by_s_codigo(s_codigo)
            if producto == None:
                count['error'] += 1
                self.aMessage.append(f"Stock: Error: No se encontró producto {s_codigo}")
                ok = False
                continue
            stock = oBStock.get_by_s_codigo(s_codigo)
            data = {
                'producto':producto,
                'n_stk_act':row['n_stk_act']
            }
            error = False
            if stock != None:
                count['update'] += 1
                if not oBStock.save(self.request, 'edit', stock.id, data):
                    error = True
                else:
                    count['update'] += 1
            else:
                if not oBStock.save(self.request, 'new', 0, data):
                    error = True
                else:
                    count['insert'] += 1

            if error:    
                count['error'] += 1
                self.aMessage.append(oBStock.message)
                ok = False


        self.aMessage.append(f"Stock: {count['insert']} insertados, {count['update']} actualizados, {count['error']} errores ")


    def import_sheets(self):
        oBCaInvDet = BCaInvDet()
        oBCaInvDet.delete_all()
        oBProducto = BProducto()
        oBProducto.delete_all()

        self.aMessage = []
        inicio = datetime.now()
        self.import_unidad_medida()
        fin = datetime.now()
        print(f"Procesado Unidades en {fin-inicio} segundos")
        print(self.aMessage)

        self.aMessage = []
        inicio = datetime.now()
        self.importar_producto()
        fin = datetime.now()
        print(f"Procesado Productos en {fin-inicio} segundos")
        print(self.aMessage)

        self.aMessage = []
        inicio = datetime.now()
        self.import_stock()
        fin = datetime.now()
        print(f"Procesado Stock en {fin-inicio} segundos")
        print(self.aMessage)
