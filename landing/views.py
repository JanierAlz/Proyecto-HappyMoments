import re
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from landing.models import ( Persona,
    Reservacion,
    MenuItems,
    MenuGrupo
)
from landing.forms import ( 
    RegistroReservaForm,
    ContactForm,
    UsuarioLoginForm,
    AgregarItemForm,
    AgregarGrupoForm
) 
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.core.mail import send_mail,mail_admins
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.views.generic import ListView
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView
)
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
from django.forms.utils import ErrorList

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: 
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])

class ReservacionListView(LoginRequiredMixin,ListView):
    login_url ='/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Reservacion
    def get_context_data(self, **kwargs):
        reservaciones = super(ReservacionListView,self).get_context_data(**kwargs)
        return reservaciones

# @login_required
# def revervas_view(request):
#     return render(request,"landing/reservas_list_view.html")


def home(request):    
    formReserva = RegistroReservaForm(request.POST or None)#,error_class=DivErrorList)
    fecha = request.POST.get('date')
    boletin = request.POST.get('newsletter')
    if not boletin:
        boletin = False
    if request.method == 'POST':
        if formReserva.is_valid():
            persona = Persona.objects.create(
                nombre= formReserva.cleaned_data['nombre'],
                apellido= formReserva.cleaned_data['apellido'],
                numero_telefono= formReserva.cleaned_data['numero_telefono'],
                correo_electronico= formReserva.cleaned_data['correo_electronico'],
                boletin_electronico= boletin
            )
            persona.save()
            reserva = Reservacion.objects.create(
                fecha_reservacion= datetime.strptime(fecha,'%d/%m/%Y'),
                hora_reservacion= formReserva.cleaned_data['hora_reservacion'],
                evento= formReserva.cleaned_data['evento'],
                numero_invitados= formReserva.cleaned_data['numero_invitados'],
            )
            reserva.save()
            persona_id = Persona.objects.get(persona_id=persona.persona_id)
            reserva.persona = persona_id
            reserva.save()
            registered_user = f"{formReserva.cleaned_data['nombre']}, {formReserva.cleaned_data['apellido']}"
            recipient = formReserva.cleaned_data['correo_electronico']
            send_mail(
                subject = f'Nueva reservacion,{registered_user}',
                message = f"""{registered_user} ha realizado una nueva reservacion para el dia {fecha}  
Motivo del evento: {formReserva.cleaned_data['evento']}.
Hora de inicio: {formReserva.cleaned_data['hora_reservacion']}
Cantidad de invitados: {formReserva.cleaned_data['numero_invitados']} 
Uno de nuestros administradores ser pondra en contacto con usted lo mas pronto posible. Debe saber que realizar solamente la reservacion
no garantiza el hecho de que se le reservara el cupo para su evento.""",
                from_email = '(NO RESPONDER) Servicio automatico de correo',
                recipient_list = [f'{recipient}']
            )
            # send_mail(
            #     subject=f'Nueva reservacion en HAPPY MOMENTS (NO RESPONDER)' ,
            #     message='''Ha realizado una reservacion en HAPPY MOMENTS, uno de nuestros administradores ser pondra en contacto con usted lo mas pronto posible. Debe saber que realizar solamente la reservacion
            #     no garantiza el hecho de que se le reservara el cupo para su evento''',
            #     from_email='Servicio automatico de correo'
            # 
            return redirect("home")
        else:
            messages.error(request,"debe ingresar los datos requeridos")
    return render(request, "landing/home.html",{"formReserva":formReserva})



def contact(request):
    contact = ContactForm(request.POST or None)
    if request.method == "POST":
        if contact.is_valid():
            mail_admins(
                subject ='Mensaje de usuario',
                message = f'''Nombre: {contact.cleaned_data['nombre']} 
                              Correo: {contact.cleaned_data['correo']}
                              Telefono: {contact.cleaned_data['telefono']}
                              Sitio web: {contact.cleaned_data['web']}
                              Mensaje: {contact.cleaned_data['mensaje']}.'''
            )
            send_mail(
                subject = 'Mensaje de contacto',
                message = "Su mensaje ha sido enviado, uno de nuestros administradores se pondra en contacto con usted lo mas pronto posible",
                from_email= '(NO RESPONDER) Servicio automatico de correo',
                recipient_list =[f'{contact.cleaned_data["correo"]}']
            )
            return redirect("home")
    else:
        return render(request,"landing/contact.html",{"contact":contact})

def about(request):
    return render(request,"landing/about.html")

def events(request):
    return render(request,"landing/events.html")

def menu(request):
    return render(request,"landing/menu.html")

def usuario_login_view(request):
    next = request.GET.get('next')
    loginForm = UsuarioLoginForm(request.POST or None)
    if request.method == "POST":
        if loginForm.is_valid():
            username = loginForm.cleaned_data.get('username')
            password = loginForm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request,user)
            if next:
                return redirect(next)
            return redirect('reservas_list_view')
        return render(request,'landing/login.html',{'loginForm':loginForm})
    else:
        return render(request,'landing/login.html',{'loginForm':loginForm})
    
def usuario_logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def cpanel_dashboard(request):
    return render(request,'landing/cpanel_dashboard.html')

class MenuGrupoCreate(CreateView):
    model = MenuGrupo
    fields = '__all__'
    template_name = 'landing/cpanel_menu_add.html'
    success_url = '/home'

class MenuGrupoUpdate(UpdateView):
    model = MenuGrupo
    fields = '__all__'

class MenuGrupoDelete(DeleteView):
    model = MenuGrupo
    success_url = reverse_lazy('home')


def menuItemAdd(request):
    itemForm= AgregarItemForm(request.POST or None)
    grupoForm= AgregarGrupoForm(request.POST or None)

    if request.method == "POST" :
        if itemForm.is_valid():
            item = itemForm.save(commit=False)
            if grupoForm.is_valid():
                grupo = grupoForm.save(commit=False)
                item.mnu_grupo_id = grupo.grupo_id
                grupo.save()
            item.save()
            return ('home')
    else:
        return render(request, 'landing/cpanel_menu_add.html', {'itemForm': itemForm, 'grupoForm': grupoForm})