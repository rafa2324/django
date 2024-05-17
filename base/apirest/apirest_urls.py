from django.urls import path
from base.apirest import apirest_view

urlpatterns = [
    path('', apirest_view.getRoutes),
    path('productos/', apirest_view.get_productos),
    path('producto/', apirest_view.get_producto),
    path('producto/<str:id>', apirest_view.get_producto),
    path('additem/', apirest_view.add_item),
    path('getinvcab/', apirest_view.get_invcab),
    path('getinvdet/<int:id_invcab>/<str:producto_codigo>', apirest_view.get_invdet),
    path('getlistinvdet/<str:id_invcab>', apirest_view.get_list_invdet),
    path('getlistinvdetu/<int:id_invcab>/<str:s_ubicacion>/<int:id_conteo>', apirest_view.get_list_invdetu),
    path('getlistinvdetugroup/<str:id_invcab>', apirest_view.get_list_invdetu_group),
]
