'''
class Template(Template)
v.1.0
Created by Edgard Ramos - ismytv@gmail.com
Date created : 2021.05.29
Updates:
    2021.07.30 : general.colors_css
    2021.08.11 : 
        obtener filename_colors_css a partir de compania.modo_apariencia
        se adiciona un parametro en el constructor license_id
    2021.08.19 :
        compania_name
'''
from ..config import aMenu, AppName
# from eventaweb.models.user import User
# from eventaweb.models.compania import Compania

class Template():
    def __init__(self, model, license_id:int=None):
        self.context = {}

        self.model = model
        self.template_container = ''
        self.template = ''

        self.template_title = ''
        self.title = ''
        if self.model != None:
            self.title = f'{AppName} - {self.model._meta.verbose_name} - Form'
        self.image_file = ''

        self.data = {}
        self.actions = {}
        self.templates_include = {}
        self.form = None
        
        # oUser = User()
        # self.filename_colors_css = oUser.get_modo_apariencia(license_id)
        self.filename_colors_css = 'styles/templates/colors_dark.css'
        #self.filename_colors_css = 'styles/templates/colors_light.css'
        # oCompania = Compania()
        # self.compania_nombre = oCompania.get_nombre(license_id)
        self.compania_nombre = ''

        self.set_context()

    def set_template_title(self, mode):
        self.template_title = f'Nuevo {self.model._meta.verbose_name.capitalize()}' if mode=='new' else f'Edición de {self.model._meta.verbose_name}'

    def set_context(self):
        self.context['general'] = {
            'template_container': self.template_container,
            'title': self.title,
            'template_title': self.template_title,
            'templates_include': self.templates_include,
            'aMenu': aMenu,
            'filename_colors_css': self.filename_colors_css,
            'compania_nombre': self.compania_nombre
        }
        self.context['data'] = self.data
        self.context['actions'] = self.actions
        self.context['form'] = self.form

   