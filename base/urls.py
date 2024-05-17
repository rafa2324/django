from django.urls import path
from base import views

# MIS CUENTAS
from base.views import home_view, login_view
from base.views import cainvcab_view, cainvdet_view
from base.api import cainvcab_api, cainvdet_api
from base.views import import_view

urlpatterns = [
    path('', home_view.main, name='main'),
    path('login/', login_view.login_app, name='login'),
    path('logout/', login_view.logout_app, name='logout'),
    path('account/', login_view.account, name='account'),
    path('register/', login_view.registerUser, name='register'),
    path('about/', login_view.about, name='about'),
    
    path('cainvcab_controller/', cainvcab_api.cainvcab_controller, name='cainvcab_controller'),

    #path('cainvcab_list/', cainvcab_view.cainvcab_list, name='cainvcab_list'),
    path('cainvcab_list/', cainvcab_view.CaInvCabView.as_view(), name='cainvcab_list'),

    path('cainvcab_form/<str:mode>/<str:id>/', cainvcab_view.cainvcab_form, name='cainvcab_form'),

    path('cainvdet_controller/', cainvdet_api.cainvdet_controller, name='cainvdet_controller'),
    path('cainvdet_list/<str:id>/', cainvdet_view.cainvdet_list, name='cainvdet_list'),
    path('cainvdet_form/<str:mode>/<str:id>/', cainvdet_view.cainvdet_form, name='cainvdet_form'),

    path('import_form/', import_view.import_data, name='import_form'),
]

