from collections import namedtuple
from enum import Enum


# from eventaweb.models.compania import Compania
# from eventaweb.routes.compania.compania_form_route import compania_form

AppName = 'AlmacénWeb'
Version = '2022.03.01.a'
CompaniaName = 'La Compañia'

UserType = namedtuple('UserType', [
                'superuser',
                'admin',
                'user'
            ])(
                superuser='S',
                admin='A',
                user='U'
            )

ActionForm = namedtuple('ActionForm', [
                'new',
                'edit',
                'delete'
            ])(
                new='new',
                edit='edit',
                delete='delete'
            )
            
ErrorCode = namedtuple('ErrorCode', [
                'ok',
                'not_found',
                'sql_error',
                'data_error',
                'exception'
            ])(*range(0,5))

            
TemplateContainerMain = namedtuple('TemplateContainerMain', [
                'container',
                'header',
                'nav',
                'footer',
                'alert_flash'
            ])(
                container = 'layout_main.html',
                header = 'header.html',
                nav = 'nav.html',
                footer = 'footer.html',
                alert_flash = 'alert_flash.html'
            )
            
TemplateContainerLogin = namedtuple('TemplateContainerLogin', [
                'container',
                'footer',
                'alert_flash'
            ])(
                container = 'layout_login.html',
                footer = 'footer.html',
                alert_flash = 'alert_flash.html'
            )

TemplateContainerGSSecondary = namedtuple('TemplateContainerGSSecondary', [
                'container',
                'header',
                'nav',
                'footer'
            ])(
                container = 'templates/layout_iafweb_secondary.html',
                header = 'main/header.html',
                nav = 'templates/nav.html',
                footer = 'templates/footer.html'
            )

Templates = namedtuple('Templates', [
                'login',
                'register',
                'account',
                'about',
                'home',
                'importar_catalogos',
                'importar_bienes',
                'importar_configuracion',
                'camas',
                'dinamica01'
            ])(
                login = 'login/login.html',
                register = 'login/register.html',
                account = 'login/account.html',
                about = 'main/about.html',
                home = 'main/home.html',
                importar_catalogos = 'configuracion/importar_catalogos.html',
                importar_bienes = 'configuracion/importar_bienes.html',
                importar_configuracion = 'configuracion/importar_configuracion.html',
                camas='datos_abiertos/camas.html',
                dinamica01='dinamica/dinamica01.html'
            )
    
Modules = namedtuple('Modules', [
                'eventaweb',
                'miscuentas',
                'stock'
        ])(*range(0,3))

LogActions = namedtuple('LogActions', [
                'login',
                'micuenta',
                'category_list',
                'product_list',
                'delete_item',
                'delete_category',
                'delete_product'
        ])(*range(0,7))

tasks = [
    { 'task':'Mi Cuenta', 'state':'Ok' },
    { 'task':'Producto', 'state':'Ok' },
    { 'task':'Categorias', 'state':'Ok'},
    { 'task':'Proveedores', 'state':'Ok'},
    { 'task':'Clientes', 'state':'Ok'},
    { 'task':'Compañia', 'state':'Ok'},
    { 'task':'Venta', 'state':'En proceso'},
    { 'task':'Compra', 'state':'En proceso'}
]

UPLOAD_FOLDER = 'static/upload/'
SHEET_NAME_CATALOGOS = '__catalogos__'
EXCEL_NAME_CONFIG = '__config__.xlsx'

Messages = namedtuple('Message', [
                'config_catalogs_not_data',
                'found',
                'not_found',
                'excel_catalogos_not_found',
                'excel_catalogos_data_error'
        ])(
            config_catalogs_not_data = 'No se encontraron datos de configuración de cátalogos',
            found = 'Encontrado',
            not_found = 'No encontrado',
            excel_catalogos_not_found = 'No se encontró archivo ' + EXCEL_NAME_CONFIG,
            excel_catalogos_data_error = 'Archivo de configuración de catálogos no es válido.'
        )

class ListaCatalogo(Enum):
    Color = 1
    Marca = 2
    UbicacionN1 = 3
    UbicacionN2 = 4
    UbicacionN3 = 5
    Responsable = 6
    Catalogo = 7
    Activo = 8
    
class Sistema():
    # responsable_ubicacion_nivel = 3     # Nivel de ubicacion para los responsables
    # responsable_ubicacion_tipo = 'desc' # Si la data viene como descripcion o codigo ('cod')
    # responsable_ubicacion_grabar_siempre = True # Graba el responsable aun si no se encuentra su ubicacion
    # responsable_activo_tipo = 'desc'    # Si la data vienen como descripcion o codigo ('cod')
    # responsable_activo_nivel_3 = True   # Cuando tipo es 'desc': si es True solo se considera la desc del N3
    igv = 18.00
    tipo_cambio = 4.10

    DIR_COMPROBANTES = 'docs'

    ESTADO_VENTA_ERROR = '0'
    ESTADO_VENTA_SAVED = '1'
    ESTADO_VENTA_PDF_GENERATED = '2'

    PROFORMA_PREFIJO = 'PROFORMA'

    UBICACION_UNICA = "UNICA"

# -------------------
# PTOVTA : 20210429
# -------------------
class Template():
    # components
    listview = 'components/listview.html'
    select = 'components/select.html'

    # log
    log_list = 'log/log_list.html'
    log_form = 'log/log_form.html'
    # cliente
    cliente_list = 'cliente/cliente_list.html'
    cliente_form = 'cliente/cliente_form.html'
    # venta
    venta_list = 'venta/venta_list.html'
    venta_form = 'venta/venta_form.html'
    venta_info = 'venta/venta_info.html'
    # compradetalle
    compradetalle_list = 'compradetalle/compradetalle_list.html'
    compradetalle_form = 'compradetalle/compradetalle_form.html'
    # cambiar password
    password_form = 'login/password_form.html'
    # compania
    compania_list = 'compania/compania_list.html'
    compania_form = 'compania/compania_form.html'
    # compra
    compra_list = 'compra/compra_list.html'
    compra_form = 'compra/compra_form.html'
    
    # categoria
    categoria_list = 'categoria/categoria_list.html'
    categoria_form = 'categoria/categoria_form.html'
    # producto
    producto_list = 'base/producto/producto_list.html'
    producto_form = 'base/producto/producto_form.html'
    # proveedor
    proveedor_list = 'proveedor/proveedor_list.html'
    proveedor_form = 'proveedor/proveedor_form.html'
    # categoria
    # producto
    categoria_list = 'base/categoria/categoria_list.html'
    categoria_form = 'base/categoria/categoria_form.html'
    
    prueba = 'prueba/prueba.html'
    dashboard = 'base/dashboard/dashboard.html'
    video_upload = 'videoteca/video_upload.html'

    room_list = 'base/room/room_list.html'
    login = 'base/login/login.html'
    account = 'base/login/account.html'
    register = 'base/login/register.html'
    about = 'base/login/about.html'
    producto_form_2 = 'base/producto/producto_form_2.html'

    ubicacion_n1_list = 'base/ubicacion/ubicacion_n1_list.html'
    ubicacion_n1_form = 'base/ubicacion/ubicacion_n1_form.html'

    # MIS CUENTAS
    banco_list = 'base/banco/banco_list.html'
    banco_form = 'base/banco/banco_form.html'
    rubrodiario_list = 'base/rubrodiario/rubrodiario_list.html'
    rubrodiario_form = 'base/rubrodiario/rubrodiario_form.html'
    conceptodiario_list = 'base/conceptodiario/conceptodiario_list.html'
    conceptodiario_form = 'base/conceptodiario/conceptodiario_form.html'
    cuenta_list = 'base/cuenta/cuenta_list.html'
    cuenta_form = 'base/cuenta/cuenta_form.html'
    cambiomoneda_list = 'base/cambiomoneda/cambiomoneda_list.html'
    cambiomoneda_form = 'base/cambiomoneda/cambiomoneda_form.html'
    movimiento_list = 'base/movimiento/movimiento_list.html'
    movimiento_form = 'base/movimiento/movimiento_form.html'
    pagosvarios_form = 'base/pagosvarios/pagosvarios_form.html'
    transferenciaspropias_form = 'base/transferenciaspropias/transferenciaspropias_form.html'

    # erdemo01
    cainvcab_list = 'base/cainvcab/cainvcab_list.html'
    cainvcab_form = 'base/cainvcab/cainvcab_form.html'
    
    cainvdet_list = 'base/cainvdet/cainvdet_list.html'
    cainvdet_form = 'base/cainvdet/cainvdet_form.html'

    import_form = 'base/import/import_form.html'

class Route():
    # log
    controller_log = '/controller_log'
    log_list = '/logs'
    log_form = '/log/<string:mode>/<int:id>'
    # cliente
    controller_cliente = '/controller_cliente'
    cliente_list = '/clientes'
    cliente_form = '/cliente/<string:mode>/<int:id>'
    # venta
    controller_venta = '/controller_venta'
    venta_list = '/ventas'
    venta_form = '/venta/<string:mode>/<int:id>'
    venta_info = '/venta/info/<string:mode>/<int:id>'
    # compradetalle
    controller_compradetalle = '/controller_compradetalle'
    compradetalle_list = '/compradetalles/<int:compra_id>'
    compradetalle_form = '/compradetalle/<string:mode>/<int:id>'
    # cambio paswword
    controller_password = '/controller_password'
    password_form = '/password'
    # compania
    controller_compania = '/controller_compania'
    compania_list = '/companias'
    compania_form = '/compania/<string:mode>/<int:id>'
    # compra
    controller_compra = '/controller_compra'
    compra_list = '/compras'
    compra_form = '/compra/<string:mode>/<int:id>'
    # categoria
    categoria_list = '/categorias'
    categoria_form = '/categoria/<string:mode>/<int:id>'
    controller_categoria = '/controller_categoria'
    # producto
    producto_list = '/productos'
    producto_form = '/producto/<string:mode>/<int:id>'
    controller_producto = '/controller_producto'
    # provedor
    proveedor_list = '/proveedores'
    proveedor_form = '/proveedor/<string:mode>/<int:id>'
    controller_proveedor = '/controller_proveedor'
    # dashboard
    dashboard = '/dashboard'
    # videoteca
    video_upload = '/video_upload'

    #ubicacion
    
class Action_old():
    def __init__(self):
        self._action_init                 = '_action_init'
        self.action_create_ventadetalle   = 'action_create_ventadetalle'
        self.action_delete_ventadetalle   = 'action_delete_ventadetalle'
        self.action_update_ventadetalle   = 'action_update_ventadetalle'
        self.action_list_productos        = 'action_list_productos'
        self.action_filter_productos      = 'action_filter_productos'
        self.action_close_modal_productos = 'action_close_modal_productos'
        self.action_cobrar                = 'action_cobrar'
        self.action_facturar              = 'action_facturar'

aMenu = [
    ('Inicio', 'main', []),

    ('Inventario', 'cainvcab_list', []),
    
    ('Import', 'import_form', []),

    # ('Catálogos', '#', [
    #    ('Bancos', '#'),
    #    ('Cuentas', '#'),
    #    ('Rubro Diario', '#'),
    #    ('Concepto Diario', '#'),
    # ]),

    # ('Operaciones', '#', [
    #     ('Cambio Moneda', '#'),
    #     ('Movimientos', '#'),
    #     ('Pagos Varios', '#'),
    #     ('Transferencias propias', '#'),

    # ]),


    # ('Inventario', '#', [
    #    ('Ubicacion N1', '#'),
    # ]),
    # ('Admistrativo', '#', [
    #    ('Cuentas por cobrar', '#'),
    #    ('Cuentas por pagar', '#'),
    #    ('Gastos', '#'),
    #    ('Tipos de gastos', '#')
    # ]),
    # ('Tienda', '#', [
    #     ('Ajuste de stock', '#'),
    #     ('Categorias', '#'),
    #     ('Compras', '#'),
    #     ('Productos', '#'),
    #     ('Proveedores', '#')
    # ]),
    # ('Facturacion', '#', [
    #     ('Clientes', '#'),
    #     ('Promociones', '#'),
    #     ('Ventas', '#')
    # ]),
    # ('Reportes', '#', [
    #     ('Balance', '#')
    # ]),
    # ('Seguridad', '#', [
    #     ('Accesos', '#'),
    #     ('Config Dashboard', '#'),
    #     ('Grupos', '#'),
    #     ('Módulos', '#'),
    #     ('Respaldos', '#'),
    #     ('Tipo de Módulos', '#'),
    #     ('Usuarios', '#')
    # ]),
    # ('Cambiar password', '#', []),
    # ('Compañia', '#', []),
    # ('Mi cuenta', '#', []),
    # ('Logs', '#', [], True),
    # ('Videoteca', '#', [
    #     ('Subir Video', '#'),
    #     ('Ver Video', '#'),
    # ]),
]


class FormaPago():
    contado = 1
    credito = 2
    aFormaPago = [
        { 'id': contado, 'desc': 'Contado' },
        { 'id': credito, 'desc': 'Crédito' }
    ]

class TipoCliente():
    persona_natural = 1
    persona_juridica = 2
    aTipoCliente = [
        { 'id': persona_natural, 'desc': 'Persona natural'},
        { 'id': persona_juridica, 'desc': 'Persona jurídica'}
    ]
    
    def get_desc(self, tipo_cliente_id):
        lista = list(filter(lambda x: x['id']==tipo_cliente_id, self.aTipoCliente))
        return lista[0]['desc'] if lista else 'no found'

class TipoComprobante():
    proforma = 0
    factura = 1
    boleta = 2
    aTipoCompobante = [
        { 'id': proforma, 'desc': 'Proforma', 'abrev': 'PRO', 'glosa':'PROFORMA' },
        { 'id': factura, 'desc': 'Factura', 'abrev': 'FAC', 'glosa':'FACTURA ELECTRONICA' },
        { 'id': boleta, 'desc': 'Boleta', 'abrev': 'BOL', 'glosa':'BOLETA DE VENTA ELECTRONICA' }
    ]

    def get_all_venta(self):
        return list(filter(lambda x:x['id']!=self.proforma, self.aTipoCompobante))

    def get_desc(self, id):
        lista = list(filter(lambda x: x['id']==id, self.aTipoCompobante))
        return lista[0]['desc'] if lista else 'no found'
    
    def get_abrev(self, id):
        lista = list(filter(lambda x: x['id']==id, self.aTipoCompobante))
        return lista[0]['abrev'] if lista else 'no found'

    def get_glosa(self, id):
        lista = list(filter(lambda x: x['id']==id, self.aTipoCompobante))
        return lista[0]['glosa'] if lista else 'no found'


class Moneda():
    soles = 1
    aMoneda = [
        { 'id': soles, 'desc': 'Soles', 'cod': 'PEN'}
    ]
    
class TipoBusquedaProducto():
    descripcion = 1
    aTipoBusquedaProducto = [
        { 'id': descripcion, 'desc': 'Por descripción'}
    ]

class SerieComprobante():
    aSerieComprobante = [
        { 'id': '001', 'desc': '001' } 
    ]

class MetodoPago():
    efectivo = 1
    debito = 2
    efectivo_debito = 3
    aMetodoPago = [
        { 'id': efectivo, 'desc': 'Efectivo' },
        { 'id': debito, 'desc': 'Débito' },
        { 'id': efectivo_debito, 'desc': 'Efectivo y Débito' }
    ]


class ImportSheet():
    producto = 'PRODUCTO'
    stock = 'STOCK'