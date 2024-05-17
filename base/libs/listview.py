''' 
class ListView(Template)
v.1.0
Created by Edgard Ramos - ismytv@gmail.com
Date created : 2021.05.29
Updates:
    2021.06.15
        Se elimina propiedad grid_columns_justify
        Se envia como: context.data.grid_columns
        Ahora la personalización de c/columna se define en el css 
        correspondiente
    2021.08.11
        se adiciona un parametro en el constructor license_id para 
        enviarselo a Template
    2022.08.21
        se adiciona atributo is_disabled_button_add por defecto es False
'''
from ..config import Template as PARAMS_Template
from ..libs.template import Template

class ListView(Template):
    ''' Clase para templates del tipo ListView
    '''
    def __init__(self, model, license_id:int=None):
        self.model = model
        self.component_listview = PARAMS_Template.listview
        self.listview_title = self.model._meta.verbose_name_plural.capitalize()
        self.listview_btn_new_text = f'Agregar {self.model._meta.verbose_name}'
        self.is_disabled_button_add = False

        self.data_grid = []
        
        self.grid_columns = []
        # self.grid_columns_justify = []          # valores del css: col, col__right, col__center
        # self.grid_columns_format_decimal = []   # false or true si tendrá formato .2f
        
        super().__init__(model, license_id)
         
        self.actions['action_new'] = ''            # personalizar url a redireccionar
        self.actions['action_edit'] = ''           # personalizar url a redireccionar
        self.actions['action_delete'] = ''         # personalizar action to controller
        self.actions['action_search'] = ''         # personalizar action to controller

        self.set_context()
        
    def set_context(self):
        ''' Define el contex. Debe llamarse antes de hacer el render 
        '''
        super().set_context()
        self.context['general']['component_listview'] = self.component_listview
        self.context['general']['listview_title'] = self.listview_title
        self.context['general']['listview_btn_new_text'] = self.listview_btn_new_text
        self.context['general']['is_disabled_button_add'] = self.is_disabled_button_add
        
        # rellena con 'col' si lista está vacía
        # self.grid_columns_justify = self.grid_columns_justify if len(self.grid_columns_justify) else \
        #                             ['col' for x in range(len(self.grid_columns))]
        # self.columns_format_decimal = self.grid_columns_format_decimal if len(self.grid_columns_format_decimal) else \
        #                             [False for x in range(len(self.grid_columns))]
        
        # self.context['grid'] = {
        #     'grid_columns' : list(zip(self.grid_columns, self.grid_columns_justify))
        # }
        self.context['data']['grid_columns'] = self.grid_columns
        
        self.context['data']['data_grid'] = self.data_grid
        
        
    def query_data(self):
        # self.model.get_all()
        # return self.model.get_aTO_toarray()
        pass
