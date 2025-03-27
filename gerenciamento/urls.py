from django.urls import path
from .views import (
    index,
    TanqueListView,
    TanqueCreateView,
    TanqueUpdateView,
    TanqueDeleteView,
    TanqueDetailView,
    AlevinoListView,
    AlevinoCreateView,
    AlevinoUpdateView,
    AlevinoDeleteView,
    InsumoListView, InsumoCreateView, InsumoUpdateView,
    InsumoDeleteView, baixa_insumo, despovoar_tanque, get_retiradas_parciais, get_notifications, marcar_notificacoes_como_lidas,
    login_view, logout_view, entrada_insumo, editar_perfil, notificacoes_view
)
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # página inicial
    path('', login_required(index), name='index'),
    # tanques
    path('tanques/', login_required(TanqueListView.as_view()), name='tanques'),
    path('tanques/novo/', login_required(TanqueCreateView.as_view()), name='tanque-create'),
    path('tanques/<int:pk>/editar/', login_required(TanqueUpdateView.as_view()), name='tanque-update'),
    path('tanques/<int:pk>/excluir/', login_required(TanqueDeleteView.as_view()), name='tanque-delete'),
    path('tanques/<int:pk>/', login_required(TanqueDetailView.as_view()), name='tanque-detail'),
    path('tanques/despovoar/', login_required(despovoar_tanque), name='tanque-despovoar'),
    path('get-retiradas-parciais/<int:pk>/',login_required(get_retiradas_parciais), name='retiradas-parciais'),
    #alevinos
    path('alevinos/', login_required(AlevinoListView.as_view()), name='alevinos'),
    path('alevinos/novo/', login_required(AlevinoCreateView.as_view()), name='alevino-create'),
    path('alevinos/editar/<int:pk>/', login_required(AlevinoUpdateView.as_view()), name='alevino-update'),
    path('alevinos/excluir/<int:pk>/', login_required(AlevinoDeleteView.as_view()), name='alevino-delete'),
    #insumos
    path('insumos/', login_required(InsumoListView.as_view()), name='insumos'),
    path('insumos/novo/', login_required(InsumoCreateView.as_view()), name='insumo-create'),
    path('insumos/editar/<int:pk>/', login_required(InsumoUpdateView.as_view()), name='insumo-update'),
    path('insumos/excluir/<int:pk>/', login_required(InsumoDeleteView.as_view()), name='insumo-delete'),
    path('insumos/dar_baixa/<int:pk>/', login_required(baixa_insumo), name='insumo-baixa'),
    path('insumo/entrada/', entrada_insumo, name='insumo-entrada'),
    #notificacao
    path('get-notifications/', login_required(get_notifications), name='get-notifications'),
    path('mark-notifications/', login_required(marcar_notificacoes_como_lidas), name='mark-notifications'),
    path('notificacoes/marcar_lidas/', marcar_notificacoes_como_lidas, name='marcar_notificacoes_como_lidas'),
    path('notificacoes/', login_required(notificacoes_view), name='notificacoes'),
    #login
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('perfil/', editar_perfil, name='perfil'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
