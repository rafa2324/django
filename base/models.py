from datetime import datetime
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
import base.choices

# Create your models here.

class Common(models.Model):
    license_id = models.IntegerField()
    user_created_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    user_edit_id = models.IntegerField(null=True, blank=True)
    date_edit = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, blank=True, default='')
  
    class Meta:
        abstract = True  


class License(Common):
    license_key = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=40)
    num_licenses = models.IntegerField(default=3)
    user_type = models.CharField(max_length=1, default='A')

    def __str__(self) -> str:
        return self.desc


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    #bio = models.TextField(null=True)
    user_type  = models.CharField(max_length=1, null=True,  default='U')
    image_file = models.ImageField(null=True, default="avatar.svg", upload_to="users/")
    license_id = models.IntegerField(default=1)
    status = models.CharField(max_length=1, default='A')
    modo_apariencia = models.CharField(max_length=1, choices = [('0', 'Claro'), ('1', 'Oscuro')], default='0')

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    pass

class Log(Common):
    modulo = models.CharField(max_length=40)
    accion = models.CharField(max_length=40)
    detalle = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.modulo} - {self.accion} - {self.detalle}'


class UnidadMedida(Common):
    s_codigo = models.CharField(max_length=5)
    s_descripcion = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.s_descripcion


class Empleado(Common):
    s_codigo = models.CharField(max_length=15)
    s_nombre_completo = models.CharField(max_length=100)

    def __str__(self) :
        return self.s_nombre_completo


class Producto(Common):
    s_codigo = models.CharField(max_length=20)
    s_descripcion = models.CharField(max_length=100)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    s_categoria = models.CharField(max_length=40, null=True)

    def __str__(self) -> str:
        return self.s_descripcion


class CaInvCab(Common):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    s_fecha_inicio = models.DateField(default=datetime.now)
    s_fecha_cierre = models.DateField(null=True, blank=True)
    s_descripcion = models.CharField(max_length=100)
    estado_inventario = models.CharField(max_length=1, choices=base.choices.EstadoInventarioChoices.choices, default='1')

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self) -> str:
        return self.s_descripcion


class CaInvDet(Common):
    ca_inv_cab = models.ForeignKey(CaInvCab, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    s_codigo = models.CharField(max_length=20)
    s_cod_barra = models.CharField(max_length=20, null=True)
    s_descripcion = models.CharField(max_length=100)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    n_stk_act = models.DecimalField(max_digits=14, decimal_places=4)
    s_ubicacion = models.CharField(max_length=10)
    ns_conteo1 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    ns_conteo2 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    s_categoria = models.CharField(max_length=40, null=True)
    unidad_medida_s_codigo = models.CharField(max_length=5, null=True)

    class Meta:
        verbose_name = 'Detalle Inventario'
        verbose_name_plural = 'Detalle Inventario'

    def __str__(self) -> str:
        return f"{self.s_descripcion} {self.ns_conteo1} {self.ns_conteo2}"


class CaInvDetU(Common):
    ca_inv_det = models.ForeignKey(CaInvDet, related_name='cainvdets', on_delete=models.CASCADE)
    id_conteo = models.IntegerField()
    s_ubicacion = models.CharField(max_length=10)
    ns_conteo = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    def __str__(self) -> str:
        return self.s_ubicacion
        #self.ca_inv_det, self.id_conteo, self.s_ubicacion, self.ns_conteo


class Stock(Common):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    n_stk_act = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    def __str__(self) -> str:
        return f'{self.producto.s_codigo} {self.n_stk_act}'

