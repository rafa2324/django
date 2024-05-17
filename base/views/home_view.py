from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from base.libs.template import Template
from base import config as PARAMS

@login_required(login_url='login')
def main(request):
    resumen_venta = {
            'count_ventas': 10,
            'count_facturas': 7,
            'count_boletas': 3,
            'total_ventas': 7000.00,
            'total_facturas': 3000.00,
            'total_boletas': 4000.00
        }
    total_compras = 1000.00
    resumen_dashboard = {
        'resumen_venta': resumen_venta,
        'resumen_balance': {
            'total_ingresos': resumen_venta['total_ventas'],
            'total_egresos': total_compras,
            'total_ganancia' : resumen_venta['total_ventas'] - total_compras
        },
        'resumen_count': {
            'count_venta': resumen_venta['count_ventas'],
            'count_categoria': 10,
            'count_cliente': 100,
            'count_producto': 70,
            'count_proveedor': 3,
        }
    }
    oTemplate = Template(None)
    oTemplate.template_title = f'{PARAMS.AppName} - Home'
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.dashboard
    oTemplate.data['resumen_venta'] = resumen_dashboard['resumen_venta']
    oTemplate.data['resumen_balance'] = resumen_dashboard['resumen_balance']
    oTemplate.data['resumen_count'] = resumen_dashboard['resumen_count']
    oTemplate.set_context()
    return render(request, oTemplate.template, context=oTemplate.context)

