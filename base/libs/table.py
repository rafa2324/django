''' 
class Table
v.1.0
Created by Edgard Ramos - ismytv@gmail.com
Date created : 2021.05.29
Updates:
Clase base para el modelo (CRUD)
    2022.08.21
        Se agrega metodo delete_all
'''

from base import config as PARAMS

class Table():
    TO = object
    message_tablename = ''  # nombre de la tabla a mostrar en message
    aTO = []                # lista de TO
    message = ''            # mensaje devuelto por crud
    message_category = ''   # categoria message (success, damger)
    error_code = -1         # codigo error devuelto por crud
    id: int

    def __init__(self) -> None:
        pass

    def get_all(self, license_id:int=None):
        '''
            Devuelve un query_all como una lista si license_id es None; en caso contrario 
            devuelve un query filtrado por la columna license_id, la cual debe existir.
        '''
        if license_id == None:
            self.aTO = self.TO.objects.all()
        else:
            self.aTO = self.TO.objects.all().filter(license_id=license_id)
        return self.aTO
    
    def get(self, id):
        try:
            oTO = self.TO.objects.get(id=int(id))
        except self.TO.DoesNotExist:
            oTO = None
        return oTO
    
    def insert(self, oTO:object):
        ok = False
        try:
            oTO.save()
            self.message = f'Se insertó correctamente.'
            ok = True
        except Exception as e:
            self.message = f'Error al insertar registro: {e}'
            self.error_code = PARAMS.ErrorCode.sql_error
        else:
            self.id = oTO.id
            self.error_code = PARAMS.ErrorCode.ok
            self.message = f'Se insertó correctamente ({self.message_tablename})'
            self.message_category = 'success'
            return True
        self.message_category = 'danger'
        return False

    def update(self, oTO:object):
        '''
            Realiza un update 
            
            Return 
                True or False.
                self.id contendrá el id del registro actualizado
                self.error_code contendrá un código de error, self.message un mensaje y 
                self.message_category el tipo de mensaje ('success', 'danger')
        '''
        try:
            oTO.save()
        except Exception as e:
            self.error_code = PARAMS.ErrorCode.sql_error
            self.message = f'Error al actualizar ({self.message_tablename}): ' + str(
                e.__dict__['orig'])
        else:
            self.id = oTO.id
            self.error_code = PARAMS.ErrorCode.ok
            self.message = f'Se actualizó correctamente ({self.message_tablename})'
            self.message_category = 'success'
            return True
        self.message_category = 'danger'
        return False

    def delete(self, id):
        oTO = self.get(id)
        if oTO == None:
            self.message = f'Ocurrió un error. No se encontró registro ({self.message_tablename}).'
            self.error_code = PARAMS.ErrorCode.not_found
        else:
            try:
                oTO.delete()
                self.message = f'Se eliminó correctamente.'
                ok = True
            except Exception as e:
                self.message = f'Error al eliminar ({self.message_tablename}): ' + str(
                    e.__dict__['orig'])
                self.error_code = PARAMS.ErrorCode.sql_error
            else:
                self.message = f'Se eliminó correctamente ({self.message_tablename}).'
                self.error_code = PARAMS.ErrorCode.ok
                self.message_category = 'success'
                return True
        self.message_category = 'danger'
        return False

    def delete_all(self):
        try:
            self.TO.objects.all().delete()
        except Exception as e:
            self.message = f'Error al eliminar ({self.message_tablename}): ' + str(
                    e.__dict__['orig'])
            self.error_code = PARAMS.ErrorCode.sql_error
        else:
            self.message = f'Se eliminó correctamente ({self.message_tablename}).'
            self.error_code = PARAMS.ErrorCode.ok
            self.message_category = 'success'
            return True
        return False


