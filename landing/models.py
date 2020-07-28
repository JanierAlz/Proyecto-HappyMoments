import uuid

from django.db import models
# from django.db.models import ForeignKey
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator
from django.urls import reverse
# Create your models here.


# class Usuario(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#     register_date = models.DateTimeField("date registered")

#     def __str__(self):
#         date_registered = timezone.localtime(self.register_date)
#         return f"date registered {date_registered.strftime('%A, %d %B, %Y at %X')}"

class Persona(models.Model):
    persona_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    numero_telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(max_length=30)
    boletin_electronico = models.BooleanField(default=False)

    def __str__(self):
        return f"""Nombre completo: {self.nombre},{self.apellido}. 
                    Telefono: {self.numero_telefono},
                    Correo Electronico: {self.correo_electronico}"""

class Reservacion(models.Model):
    TIPO_EVENTO = [
    ('cumpleaños','Cumpleaños'),
    ('empresarial','Fiestas Coorporativas'),
    ('social','Reuniones Sociales'),
    ('especiales','Eventos Especiales'),
]
    HORARIO = [
    ('11:00','11:00 am'),
    ('11:30','11:30 am'),
    ('12:00','12:00 pm'),        
    ('12:30','12:30 pm'),
    ('13:00','1:00 pm'),
    ('13:30','1:30 pm'),
    ('14:00','2:00 pm'),
    ('14:30','2:30 pm'),
    ('15:00','3:00 pm'),
    ('15:30','3:30 pm'),
    ('16:00','4:00 pm'),
    ('16:30','4:30 pm'),
    ('17:00','5:00 pm'),
    ('17:30','5:30 pm'),
    ('18:00','6:00 pm'),
    ('18:30','6:30 pm'),
    ('19:00','7:00 pm'),
    ('19:30','7:30 pm'),
    ('20:00','8:00 pm'),
    ('20:30','8:30 pm'),
    ('21:00','9:00 pm'),
    ('21:30','9:30 pm'),
    ('22:00','10:00 pm'),
    ('22:30','10:30 pm'),
    ('23:00','11:00 pm'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, editable=False, null=True)
    reservacion_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    fecha_reservacion = models.DateField()
    hora_reservacion = models.CharField(choices=HORARIO, max_length=15)
    # TipoEvento = models.TextChoices('TipoEvento','EMPRESARIAL SOCIAL NIÑOS ADOLECENTES FESTIVO')
    evento = models.CharField(choices=TIPO_EVENTO, max_length=15)
    numero_invitados = models.IntegerField()

    def __str__(self):
        return f"""{Persona.nombre}, {Persona.apellido} 
        fecha de reservacion:{self.fecha_reservacion}
        tipo de evento: {self.evento}"""

class MenuGrupo(models.Model):
    grupo_id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=20)
    grupo_activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre}"
    

class MenuItems(models.Model):
    mnu_item_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    mnu_grupo = models.ForeignKey(MenuGrupo, on_delete= models.CASCADE, null=True)
    mnu_item_nombre = models.CharField(max_length=20)
    mnu_item_detalles = models.TextField(max_length=300)
    mnu_item_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.mnu_item_nombre}"