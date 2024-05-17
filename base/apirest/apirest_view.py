from email.policy import HTTP
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.html import escape

from ..business.bcainvdetu import BCaInvDetU
from ..business.bcainvcab import BCaInvCab
from base.business.bproducto import BProducto
from .serializer import ProductoSerializer
from base.models import CaInvCab, CaInvDet
from base.choices import EstadoInventarioChoices
from base.business.bcainvdet import BCaInvDet
from base.config import Sistema
from base.business.blog import BLog


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/getinvcab/',
        'POST /api/additem/',
        'GET /api/getinvdet/id_invcab/producto_codigo',
        'GET /api/getlistinvdet/id_invcab',
        'GET /api/getlistinvdetu/id_invcab/s_ubicacion/id_conteo',
        'GET /api/getlistinvdetugroup/id_invcab',
    ]
    return Response(routes)

@api_view(['GET'])
def get_productos(request):
    oBProducto = BProducto()
    productos = oBProducto.get_all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def get_producto(request, id=None):
    if request.method == 'GET':
        oBProducto = BProducto()
        producto = oBProducto.get(id)
        serializer = ProductoSerializer(producto, many=False)
        data_response = {
            'status' : status.HTTP_200_OK if producto is not None else status.HTTP_204_NO_CONTENT,
            'data' : serializer.data if producto is not None else {}
        }
        return Response(data_response)
    
    elif request.method == 'POST':
        print('POST', request.data)
        return Response({})


@api_view(['POST'])
def add_item(request):
    # print('POST api/additem', request.data)
    print(request, request.data)
    
    #oBLOg = BLog()
    
    try:
        data = request.data
        ca_inv_cab_id = data['ca_inv_cab_id']
        id_conteo = data['id_conteo']
        producto_codigo = data['producto_codigo']
        s_ubicacion = data['s_ubicacion']
        cantidad = data['cantidad']

        # oBLOg.save(None, 'new', 0, {'modulo':'api', 'accion':'getadditem', 
        #     'detalle': f'request: {ca_inv_cab_id} - {producto_codigo} - {s_ubicacion} - {cantidad}'})

        if len(s_ubicacion) == 0:
            s_ubicacion = Sistema.UBICACION_UNICA

        oBCaInvCab = BCaInvCab()
        if not oBCaInvCab.add_item(
            ca_inv_cab_id, 
            producto_codigo, 
            s_ubicacion, 
            cantidad, 
            id_conteo):
            status_id = status.HTTP_404_NOT_FOUND
            message = oBCaInvCab.message 
        else:
            status_id = status.HTTP_200_OK
            message = 'OK'

        data_response = {
            'status' : status_id,
            'data' : data,
            'message': message
        }

        # oBLOg.save(None, 'new', 0, 
        #     {'modulo':'api', 'accion':'getadditem', 
        #     'detalle':f'response: OK - {ca_inv_cab_id} - {producto_codigo} - {s_ubicacion} - {cantidad}' if status_id==status.HTTP_200_OK else f'response ERROR {message}'
        #     }
        # )

    except Exception as e:
        data_response = {
            'status' : status.HTTP_400_BAD_REQUEST ,
            'data' : {},
            'message': f'Ocurrió un error except. {e}' 
        }
        # oBLOg.save(None, 'new', 0, 
        #     {'modulo':'api', 'accion':'getadditem', 
        #     'detalle':f'response: OK - {data_response["status"]} - {data_response["message"]}'
        #     }
        # )

    return Response(data_response)


@api_view(['GET'])
def get_invcab(request):
    print(request)

    aTO = CaInvCab.objects.all().filter(estado_inventario=EstadoInventarioChoices.opened)
    if aTO:
        oTO:CaInvCab = aTO[0] 
        data_response = {
            'status': status.HTTP_200_OK,
            'data': {
                'id': oTO.id,
                's_descripcion': oTO.s_descripcion,
                'empleado_nombre_copleto': oTO.empleado.s_nombre_completo,
                's_fecha_inicio': oTO.s_fecha_inicio
            }
        }
    else:
        data_response = {
            'status': status.HTTP_204_NO_CONTENT,
            'data': {}
        }

    return Response(data_response)

@api_view(['GET'])
def get_invdet(request, id_invcab:int, producto_codigo:str):
    print(request)

    # print(request.META['SESSION_MANAGER'])
    # print(request.META['REMOTE_ADDR'])
    # print(request.META['REMOTE_HOST'])
    # print(request.META['SERVER_NAME'])
    # print(request.META['QUERY_STRING'])
    # print(request.META['HTTP_USER_AGENT'])
    # print(request.META['HTTP_HOST'])
    # print(request.META['CONTENT_TYPE'])
    # print(request.headers['User-Agent'])
    

    producto_codigo = escape(producto_codigo)

    oBCaInvDet = BCaInvDet()
    oTO:CaInvDet = oBCaInvDet.get_item(id_invcab, producto_codigo)
    if oTO == None:
        data_response = {
            'status': status.HTTP_204_NO_CONTENT,
            'data' : {}
        }
    else:
        data_response = {
            'status': status.HTTP_200_OK,
            'data' : oBCaInvDet.get_oTO_toDict(oTO)
            # 'data': {
            #     'id': oTO.producto.id,
            #     's_descripcion': oTO.s_descripcion,
            #     's_codigo': oTO.producto.s_codigo,
            #     'unidad_medida_s_codigo': oTO.unidad_medida.s_codigo,
            #     'unidad_medida_s_descripcion': oTO.unidad_medida.s_descripcion,
            #     'n_stk_act': oTO.n_stk_act,
            #     'ns_conteo1': oTO.ns_conteo1,
            #     'ns_conteo2': oTO.ns_conteo2,

            # }
        }
    return Response(data_response)


@api_view(['GET'])
def get_list_invdet(request, id_invcab):
    print(request)

    oBCaInvDet = BCaInvDet()
    oBCaInvDet.get_all_invcab(id_invcab)
    aCaInvDet = oBCaInvDet.get_aTO_toArray()
    if not aCaInvDet:
        data_response = {
            'status': status.HTTP_204_NO_CONTENT,
            'data' : []
        }
    else:
        data_response = {
            'status': status.HTTP_200_OK,
            'data': aCaInvDet
        }
    return Response(data_response)


@api_view(['GET'])
def get_list_invdetu(request, id_invcab, s_ubicacion, id_conteo):
    print(request)

    oBCaInvDetU = BCaInvDetU()
    oBCaInvDetU.get_all_inv_ubi_conteo(id_invcab, s_ubicacion, id_conteo)
    aCaInvDetU = oBCaInvDetU.get_aTO_toArray()
    if not aCaInvDetU:
        data_response = {
            'status': status.HTTP_204_NO_CONTENT,
            'data' : []
        }
    else:
        data_response = {
            'status': status.HTTP_200_OK,
            'data': aCaInvDetU
        }
    return Response(data_response)


@api_view(['GET'])
def get_list_invdetu_group(request, id_invcab):
    print(request)

    oBCaInvDetU = BCaInvDetU()
    aCaInvDetU = oBCaInvDetU.get_all_ubi_group(id_invcab)
    #aCaInvDetU = oBCaInvDetU.get_aTO_toArray()
    if not aCaInvDetU:
        data_response = {
            'status': status.HTTP_204_NO_CONTENT,
            'data' : []
        }
    else:
        data_response = {
            'status': status.HTTP_200_OK,
            'data': aCaInvDetU
        }
    return Response(data_response)

