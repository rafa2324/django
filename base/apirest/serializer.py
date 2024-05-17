from rest_framework.serializers import ModelSerializer
from base.models import Producto
from base.models import CaInvCab


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        
    
class CaInvCabSerializer(ModelSerializer):
    class Meta:
        model = CaInvCab
        fields = '['