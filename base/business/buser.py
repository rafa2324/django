from base import config as PARAMS

class BUser():
    aTO = []                # lista de TO
    message = ''            # mensaje devuelto por crud
    aMessage = []           # lista de mensajes
    message_category = ''   # categoria message (success, damger)
    error_code = -1         # codigo error devuelto por crud

    def save(self, form):
        ok = False
        try:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            ok = True
            self.message = f'Se insertó correctamente.'
        except Exception as e:
            self.message = f'Error al insertar registro: {e}'
            self.error_code = PARAMS.ErrorCode.sql_error
        
        return user if ok else None