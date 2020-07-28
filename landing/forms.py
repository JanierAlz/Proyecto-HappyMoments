from django import forms
from landing.models import (Persona, 
    Reservacion, 
    MenuGrupo, 
    MenuItems
)
from django.contrib.auth import authenticate
from django.core.validators import (
    RegexValidator,
    EmailValidator
)

class RegistroReservaForm(forms.Form):
    nombre = forms.CharField(label="")
    apellido = forms.CharField(label="")
    numero_telefono = forms.CharField(label="",validators=[RegexValidator('^\+?[0-9][-\s]?[0-9][-\s]?[0-9][-\s]?[0-9]',message="el numero que ingreso es invalido")])
    correo_electronico = forms.EmailField(label="")
    numero_invitados = forms.IntegerField(label="",min_value= 0)
    evento = forms.ChoiceField(label="Tipo de evento",choices=Reservacion.TIPO_EVENTO)
    hora_reservacion = forms.ChoiceField(label="Hora de inicio",choices=Reservacion.HORARIO)

    def __init__(self, *args, **kwargs):
        super(RegistroReservaForm,self).__init__(*args, **kwargs)
        self.fields['hora_reservacion'].widget.attrs.update({'placeholder':'Hora de Inicio'})
        self.fields['hora_reservacion'].required= True
        self.fields['evento'].widget.attrs.update({'placeholder':'Ocasion del evento'})
        self.fields['numero_invitados'].widget.attrs.update({'placeholder':'# Estimado de Invitados'})
        self.fields['numero_invitados'].required=True
        self.fields['nombre'].widget.attrs.update({'placeholder':'Nombre'})
        self.fields['nombre'].required = True
        self.fields['apellido'].widget.attrs.update({'placeholder':'Apellido'})
        self.fields['apellido'].required = True
        self.fields['numero_telefono'].widget.attrs.update({'placeholder':'Telefono'})
        self.fields['numero_telefono'].required= True
        self.fields['correo_electronico'].widget.attrs.update({'placeholder':'Email: ejemplo@example.com', 'size':20})
        self.fields['correo_electronico'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs['class']= 'form-control'

    # def clean(self, *args, **kwargs):
    #     nombre = self.cleaned_data.get('nombre')
    #     apellido = self.cleaned_data.get('apellido')
    #     numero_telefono = self.cleaned_data.get('numero_telefono')
    #     numero_invitados = self.cleaned_data.get('numero_invitados')
    #     correo_electronico = self.cleaned_data.get('correo_electronico')
    #     campos = [nombre,apellido,numero_telefono,numero_invitados, correo_electronico]
    #     if not all(campos):
    #         raise forms.ValidationError('Debe ingresar un todos los campos requeridos')
    #     return super(RegistroReservaForm, self).clean(*args, **kwargs)
    
    # def clean_correo_electronico(self):
    #     correo = self.cleaned_data['correo_electronico']
        
    #     if not correo.endswith('@hotmail.com'):
    #         raise forms.ValidationError('El correo no es valido')
        
    #     return correo



class ContactForm(forms.Form):
    nombre = forms.CharField()
    correo = forms.EmailField()
    telefono = forms.CharField()
    web = forms.CharField()
    mensaje = forms.CharField(widget=forms.Textarea)

    #Custom Widgets
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'placeholder':'Nombre y Apellido'})
        self.fields['nombre'].required = True
        self.fields['correo'].widget.attrs.update({'placeholder':'Email'})
        self.fields['correo'].required = True
        self.fields['telefono'].widget.attrs.update({'placeholder':'Telefono (opcional)'})
        self.fields['telefono'].required= False
        self.fields['web'].widget.attrs.update({'placeholder':'Sitio Web (opcional)'})
        self.fields['web'].required = False
        self.fields['mensaje'].widget.attrs.update({'placeholder': 'Escribe tu mensaje aca .....'})
        self.fields['mensaje'].required = True
    


class UsuarioLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError("El usuario no existe")
            if not user.check_password(password):
                raise forms.ValidationError("Clave incorrecta")
            if not user.is_active:
                raise forms.ValidationError("El usuario no se encuentra activo")
        return super(UsuarioLoginForm, self).clean(*args, **kwargs)

class AgregarItemForm(forms.ModelForm):
    MENU_GRUPO = MenuGrupo.objects.values_list('grupo_id', 'nombre')
    mnu_item_nombre = forms.CharField(max_length=20)
    mnu_item_detalles = forms.CharField(widget=forms.Textarea)
    mnu_grupo_id = forms.ChoiceField(label="",choices=MENU_GRUPO, )
    class Meta:
        model = MenuItems
        fields = ('mnu_item_nombre','mnu_item_detalles')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mnu_item_nombre'].widget.attrs.update({'placeholder':'Nombre', 'required': True})
        self.fields['mnu_item_nombre'].widget.attrs.update(style='max-width:20em; font-size:12px; padding:10px;')
        self.fields['mnu_item_detalles'].widget.attrs.update({'placeholder':'Descripcion', 'required': True})
        self.fields['mnu_grupo_id'].widget.attrs.update(style='font-size:12px; width:240px; height:38px; margin-bottom:5px; padding:10px')

class AgregarGrupoForm(forms.ModelForm):
    class Meta:
        model = MenuGrupo
        fields = '__all__'