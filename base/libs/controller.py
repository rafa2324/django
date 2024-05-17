class Controller():
    '''
        Clase controlador para manejar las solicitudes recibidads del front-end (fetch)
        Requiere:
            diccionario recibido en la solicitud : data
            debe contener al menos un key = 'action'
    '''
    data : dict()       # dict del request 
    action: str         # data['action']
    actions : dict()    # acciones { 'key_action' : method }
    context : dict()    # dict a devolver 
    
    def __init__(self, data):
        self.data = data
        self.action = data['action']
        self.context = {
            'action' : self.action,
            'status' : 200,
            'aMessage' : []
        }
        self.set_actions()
        
    
    def set_actions(self):
        '''
            Se definen todas las acciones que manejará el controlador. 
            Por defecto siempre tendrá la accion _action_init. 
            Para personalizar las acciones, implementar éste método en el controller heredado
        '''
        self.actions = {
            '_action_init' : self.action_init
        }
        self.actions['action_save'] = self.action_save
        self.actions['action_delete'] = self.action_delete
        self.actions['action_refresh'] = self.action_refresh
        self.actions['action_edit'] = self.action_edit
        
    def get_actions(self):
        actions = { x : x for x in self.actions.keys() }
        print('--actions--', actions)
        return actions
        
    def action_init(self):
        # diccionario de acciones
        self.context['actions'] = self.get_actions()
        # personalizar 
        
    def do_action(self):
        '''
            Obtiene al método correspondiente de la accion self.action y lo ejecuta.
            Dicho método actualiza self.context
            Si no existe metodo asociado, self.context se actualiza con un status de error
            
            Retorna: 
                self.context
        '''
        index = list(self.actions.keys()).index(self.action)
        if index >= 0:
            list(self.actions.values())[index]() 
        else:
            self.context['status'] = -100
            self.context['aMessage'].append(f'Error: Acción no definida ({self.action}).')
        return self.context

    def action_save(self):
        return self.context
    
    def action_edit(self):
        return self.context
    
    def action_refresh(self):
        return self.context
    
    def action_delete(self):
        return self.context