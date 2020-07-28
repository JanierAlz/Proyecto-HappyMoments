from django.urls import path
from django.contrib import admin
from landing import views
from landing.models import Persona,Reservacion


# home_list_views = views.HomeListView.as_view(
#     queryset = LogMessage.objects.order_by("-log_date")[:5],
#     context_object_name = "message_list",
#     template_name = "landing/home.html"
# )

# home_user_views = views.HomeUserViews.as_view(
#     queryset = Usuario.objects.order_by("-register_date")[:5],
#     context_object_name = "user_list",
#     template_name = "landing/registered_list.html"
# )

reservacion_list_view = views.ReservacionListView.as_view(
    queryset = Reservacion.objects.all(),
    context_object_name = "reservas_list",
    template_name = "landing/reservas_list_view.html"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("home/",views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("events/",views.events, name="events"),
    path("menu/",views.menu,name="menu"),
    path("accounts/login/", views.usuario_login_view, name='login'),
    path("accounts/logout", views.usuario_logout_view, name="logout"),
    path("reservas_list_view/", reservacion_list_view, name='reservas_list_view'),
    path("cpanel_dashboard/", views.cpanel_dashboard, name="dashboard"),
    path("menu/add/", views.menuItemAdd, name='menu-add'),
    path("menu/<int:mnu_grupo_id>", views.MenuGrupoUpdate.as_view(), name="menu-update"),
    path("menu/<int:mnu_grupo_id>/delete", views.MenuGrupoDelete.as_view(), name="menu-delete"),
]

