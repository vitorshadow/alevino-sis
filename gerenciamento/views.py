from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django_filters.views import FilterView
from .models import Tanque, Alevino, Insumo, RetiradaParcial, HistoricoTanque, Notificacao
from .forms import TanqueForm, AlevinoForm, InsumoForm
from django.http import JsonResponse
from datetime import timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm





def get_retiradas_parciais(request, pk):
    tanque = get_object_or_404(Tanque, pk=pk)
    retiradas = list(tanque.retiradas_parciais.all().values('data', 'quantidade'))
    return JsonResponse({'retiradas': retiradas})


#página home
def index(request):
    total_tanques = Tanque.objects.count()
    return render(request, 'gerenciamento/index.html', {'total_tanques': total_tanques})


#tanques

class TanqueListView(FilterView, ListView):
    model = Tanque
    template_name = 'gerenciamento/tanques/tanques.html'
    context_object_name = 'tanques'
    filterset_fields = ['especie_alevino', 'data_povoamento', 'data_retirada']
    paginate_by = 10  # Paginação


    def get_queryset(self):
        user_group = self.request.user.groups.first()  
        queryset = Tanque.objects.all()

        if user_group:
            queryset = queryset.filter(grupo=user_group) | queryset.filter(grupo__isnull=True)

        search_query = self.request.GET.get('search', '')
        estado_filtro = self.request.GET.get('estado_filtro', '')
        sort_field = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')
        tipo_data = self.request.GET.get('tipo_data', '')
        data_inicio = self.request.GET.get('data_inicio', '')
        data_fim = self.request.GET.get('data_fim', '')

        if search_query:
            queryset = queryset.filter(Q(id_tanque__icontains=search_query))

        # 🔥 Correção da lógica da cor do estado
        queryset = queryset.annotate(
            estado_num=Case(
                # 🔴 Vermelho (crítico): se a previsão de retirada já passou ou falta menos de 3 dias
                When(previsao_retirada__lt=now().date(), then=Value(1)),  
                When(previsao_retirada__lte=now().date() + timedelta(days=3), then=Value(1)),  

                # 🟡 Amarelo (atenção): se faltam entre 4 e 7 dias
                When(previsao_retirada__lte=now().date() + timedelta(days=7), then=Value(2)),  

                # 🟢 Verde (seguro): se falta mais de 7 dias
                When(previsao_retirada__gt=now().date() + timedelta(days=7), then=Value(3)),  

                default=Value(4),  
                output_field=IntegerField(),
            )
        )

        if estado_filtro:
            estados_dict = {"vermelho": 1, "amarelo": 2, "verde": 3}
            if estado_filtro in estados_dict:
                queryset = queryset.filter(estado_num=estados_dict[estado_filtro])

        if tipo_data and (data_inicio or data_fim):
            if tipo_data == "povoamento":
                if data_inicio:
                    queryset = queryset.filter(data_povoamento__gte=data_inicio)
                if data_fim:
                    queryset = queryset.filter(data_povoamento__lte=data_fim)
            elif tipo_data == "retirada":
                if data_inicio:
                    queryset = queryset.filter(previsao_retirada__gte=data_inicio)
                if data_fim:
                    queryset = queryset.filter(previsao_retirada__lte=data_fim)

        if order == "desc":
            queryset = queryset.order_by(f"-{sort_field}")
        else:
            queryset = queryset.order_by(f"{sort_field}")

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tanques = self.get_queryset() 

        context['form'] = TanqueForm()
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'id')
        context['current_order'] = self.request.GET.get('order', 'asc')
        context['estado_filtro'] = self.request.GET.get('estado_filtro', '')

     
        context['tipo_data'] = self.request.GET.get('tipo_data', '')
        context['data_inicio'] = self.request.GET.get('data_inicio', '')
        context['data_fim'] = self.request.GET.get('data_fim', '')

        
        for tanque in tanques:
            if tanque.previsao_retirada:
                dias_restantes = (tanque.previsao_retirada - now().date()).days
                if dias_restantes < 0:
                    tanque.estado_cor = "bg-danger"  
                elif dias_restantes < 7:
                    tanque.estado_cor = "bg-warning"  
                else:
                    tanque.estado_cor = "bg-success" 
            else:
                tanque.estado_cor = "bg-secondary" 

   
        paginator = Paginator(tanques, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            context['tanques'] = paginator.page(page)
        except PageNotAnInteger:
            context['tanques'] = paginator.page(1)
        except EmptyPage:
            context['tanques'] = paginator.page(paginator.num_pages)

        return context



class TanqueCreateView(CreateView):
    model = Tanque
    form_class = TanqueForm
    template_name = 'gerenciamento/tanques/create_tanques.html'
    success_url = reverse_lazy('tanques')

    def form_valid(self, form):
        form.instance.grupo = self.request.user.groups.first()  # Define o grupo do usuário logado
        return super().form_valid(form)

class TanqueUpdateView(UpdateView):
    model = Tanque
    form_class = TanqueForm
    template_name = 'gerenciamento/tanques/update_tanques.html'
    success_url = reverse_lazy('tanques')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()  # Garante a instância correta
        return kwargs

class TanqueDeleteView(DeleteView):
    model = Tanque
    template_name = 'gerenciamento/tanques/delete_tanques.html'
    success_url = reverse_lazy('tanques')

class TanqueDetailView(DetailView):
    model = Tanque
    template_name = 'gerenciamento/tanques/detail_tanques.html'
    context_object_name = 'tanque'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tanque = self.get_object()

        # Pegando parâmetros da requisição GET
        sort_field = self.request.GET.get('sort', 'data_real_retirada')  # Ordenação padrão
        order = self.request.GET.get('order', 'asc')
        tipo_data = self.request.GET.get('tipo_data', '')  # Novo: Tipo de data
        data_inicio = self.request.GET.get('data_inicio', '')
        data_fim = self.request.GET.get('data_fim', '')

        # Obtendo o histórico filtrado
        historico = tanque.historico_baixas.all()

        # Aplicando filtro por intervalo de datas
        if tipo_data == "povoamento":
            if data_inicio:
                historico = historico.filter(data_povoamento__gte=data_inicio)
            if data_fim:
                historico = historico.filter(data_povoamento__lte=data_fim)
        elif tipo_data == "retirada":
            if data_inicio:
                historico = historico.filter(data_real_retirada__gte=data_inicio)
            if data_fim:
                historico = historico.filter(data_real_retirada__lte=data_fim)
        elif tipo_data == "previsao":
            if data_inicio:
                historico = historico.filter(previsao_retirada__gte=data_inicio)
            if data_fim:
                historico = historico.filter(previsao_retirada__lte=data_fim)

        # Aplicando ordenação
        if sort_field == "taxa_sobrevivencia":
            sort_field = "taxa_sobrevivencia"

        if order == "desc":
            historico = historico.order_by(f"-{sort_field}")
        else:
            historico = historico.order_by(sort_field)

        # Passando os dados para o template
        context['historico'] = historico
        context['current_sort'] = sort_field
        context['current_order'] = order
        context['tipo_data'] = tipo_data
        context['data_inicio'] = data_inicio
        context['data_fim'] = data_fim

        return context



#alevino

class AlevinoListView(FilterView, ListView):
    model = Alevino
    template_name = 'gerenciamento/alevinos/alevinos.html'
    context_object_name = 'alevinos'
    filterset_fields = ['especie']
    paginate_by = 10

    #restringir acesso apenas ao grupo que pertence
    def get_queryset(self):
        user_group = self.request.user.groups.first()
        return Alevino.objects.filter(grupo=user_group)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        sort_field = self.request.GET.get('sort', 'especie')  # Define a ordenação padrão como 'especie'
        order = self.request.GET.get('order', 'asc')

        if search_query:
            queryset = queryset.filter(Q(especie__icontains=search_query))

        if order == "desc":
            sort_field = f"-{sort_field}"

        return queryset.order_by(sort_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AlevinoForm() 
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'especie')
        context['current_order'] = self.request.GET.get('order', 'asc')
        return context
    
class AlevinoCreateView(CreateView):
    model = Alevino
    form_class = AlevinoForm
    template_name = 'gerenciamento/alevinos/create_alevinos.html'
    success_url = reverse_lazy('alevinos')

    def form_valid(self, form):
        form.instance.grupo = self.request.user.groups.first()
        return super().form_valid(form)


class AlevinoUpdateView(UpdateView):
    model = Alevino
    form_class = AlevinoForm
    template_name = 'gerenciamento/alevinos/update_alevinos.html'
    success_url = reverse_lazy('alevinos')

class AlevinoDeleteView(DeleteView):
    model = Alevino
    template_name = 'gerenciamento/alevinos/delete_alevinos.html'
    success_url = reverse_lazy('alevinos')

#insumos

class InsumoListView(ListView):
    model = Insumo
    template_name = 'gerenciamento/insumos/insumos.html'
    context_object_name = 'insumos'
    paginate_by = 10  

    def get_queryset(self):
        user_group = self.request.user.groups.first()  # 🔥 Garante que só veja insumos do grupo dele
        queryset = Insumo.objects.filter(grupo=user_group) if user_group else Insumo.objects.all()

        # Parâmetros da URL
        search_query = self.request.GET.get('search', '')
        estado_filtro = self.request.GET.get('estado_filtro', '')
        sort_field = self.request.GET.get('sort', 'nome_produto')
        order = self.request.GET.get('order', 'asc')
        data_inicio = self.request.GET.get('data_inicio', '')
        data_fim = self.request.GET.get('data_fim', '')

        # 🔍 Filtro por nome do insumo
        if search_query:
            queryset = queryset.filter(Q(nome_produto__icontains=search_query))

        # 📌 Filtro por Data de Compra
        if data_inicio:
            queryset = queryset.filter(data_compra__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_compra__lte=data_fim)

        # 📌 Anotando Estado (Vermelho ou Verde)
        queryset = queryset.annotate(
            estado_num=Case(
                When(quantidade_produto__lte=F('estoque_minimo'), then=Value(1)),  # 🔴 Crítico
                When(quantidade_produto__gt=F('estoque_minimo'), then=Value(2)),  # 🟢 Seguro
                default=Value(2),
                output_field=IntegerField(),
            )
        )

        # ✅ Aplicando filtro de estado
        if estado_filtro:
            estados_dict = {"vermelho": 1, "verde": 2}
            if estado_filtro in estados_dict:
                queryset = queryset.filter(estado_num=estados_dict[estado_filtro])

        # 🔄 Ordenação
        queryset = queryset.order_by(f"-{sort_field}") if order == "desc" else queryset.order_by(f"{sort_field}")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InsumoForm()  # 🔥 Agora o formulário é passado para o template!

        # Parâmetros da URL para filtros e ordenação
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'nome_produto')
        context['current_order'] = self.request.GET.get('order', 'asc')
        context['estado_filtro'] = self.request.GET.get('estado_filtro', '')
        context['data_inicio'] = self.request.GET.get('data_inicio', '')
        context['data_fim'] = self.request.GET.get('data_fim', '')

        # 🔄 Paginação
        insumos = self.get_queryset()
        paginator = Paginator(insumos, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            context['insumos'] = paginator.page(page)
        except PageNotAnInteger:
            context['insumos'] = paginator.page(1)
        except EmptyPage:
            context['insumos'] = paginator.page(paginator.num_pages)

        return context






class InsumoCreateView(CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'gerenciamento/insumos/create_insumos.html'
    success_url = reverse_lazy('insumos')

    def form_valid(self, form):
        form.instance.grupo = self.request.user.groups.first()
        return super().form_valid(form)


class InsumoUpdateView(UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'gerenciamento/insumos/update_insumos.html'
    success_url = reverse_lazy('insumos')

class InsumoDeleteView(DeleteView):
    model = Insumo
    template_name = 'gerenciamento/insumos/delete_insumos.html'
    success_url = reverse_lazy('insumos')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def baixa_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    
    if request.method == "POST":
        quantidade = int(request.POST.get("quantidade", 0))
        
        if quantidade > insumo.quantidade_produto:
            messages.error(request, "Quantidade maior do que disponível no estoque.")
        else:
            insumo.quantidade_produto -= quantidade
            insumo.save()
            messages.success(request, "Baixa realizada com sucesso!")

        return redirect('insumos')  # Redireciona de volta para a lista de insumos
    
    return render(request, 'gerenciamento/insumos/insumos.html', {'insumo': insumo})


def entrada_insumo(request):
    if request.method == "POST":
        insumo_id = request.POST.get("insumo_id")
        quantidade = int(request.POST.get("quantidade_entrada", 0))
        
        insumo = get_object_or_404(Insumo, id=insumo_id)

        if quantidade > 0:
            insumo.quantidade_produto += quantidade
            insumo.save()
            messages.success(request, f"{quantidade} unidades adicionadas ao insumo {insumo.nome_produto}!")
        else:
            messages.error(request, "A quantidade deve ser maior que zero!")

    return redirect('insumos')

# despovoar
"""
def despovoar_tanque(request):
    if request.method == 'POST':
        tanque = get_object_or_404(Tanque, id=request.POST.get('tanque_id'))
        
        if 'finalizar' in request.POST:
            # Soma todas as retiradas parciais
            total_retirado = sum(r.quantidade for r in tanque.retiradas_parciais.all())

            HistoricoTanque.objects.create(
                tanque=tanque,
                especie=tanque.especie_alevino.especie if tanque.especie_alevino else "Desconhecida",
                quantidade_povoada=tanque.quantidade_povoada,
                quantidade_despovoada=total_retirado,
                data_povoamento=tanque.data_povoamento,
                previsao_retirada=tanque.previsao_retirada,
                data_real_retirada=request.POST.get('data_final'),
                taxa_sobrevivencia=tanque.taxa_sobrevivencia or 0
            )
            
            tanque.quantidade_retirada = total_retirado
            tanque.data_retirada = request.POST.get('data_final')
            tanque.ativo = False
            tanque.save()
            
            # Limpa as retiradas parciais
            tanque.retiradas_parciais.all().delete()
            return redirect('tanques')
            
        else:
            # Adiciona retirada parcial
            RetiradaParcial.objects.create(
                tanque=tanque,
                quantidade=request.POST.get('quantidade_parcial'),
                data=request.POST.get('data_parcial')
            )
            return redirect('tanques')
    
    return redirect('tanques')
"""

def despovoar_tanque(request):
    if request.method == 'POST':
        tanque = get_object_or_404(Tanque, id=request.POST.get('tanque_id'))
        quantidade_retirada = int(request.POST.get('quantidade_retirada', 0))
        data_retirada = request.POST.get('data_final')

        if quantidade_retirada > tanque.quantidade_povoada:
            messages.error(request, "A quantidade retirada não pode ser maior que a povoada.")
            return redirect('tanques')

        # Criar o histórico antes de limpar os campos
        HistoricoTanque.objects.create(
            tanque=tanque,
            especie=tanque.especie_alevino.especie if tanque.especie_alevino else "Desconhecida",
            quantidade_povoada=tanque.quantidade_povoada,
            quantidade_despovoada=quantidade_retirada,
            data_povoamento=tanque.data_povoamento,
            previsao_retirada=tanque.previsao_retirada,
            data_real_retirada=data_retirada,
            taxa_sobrevivencia=(quantidade_retirada / tanque.quantidade_povoada) * 100 if tanque.quantidade_povoada else 0,
            grupo=tanque.grupo
        )

        # 🛑 Agora limpamos os dados para indicar que o tanque está desocupado (mas sem usar None)
        tanque.especie_alevino = None
        tanque.quantidade_povoada = 0  # Definir como 0 em vez de None
        tanque.data_povoamento = None
        tanque.previsao_retirada = None
        tanque.quantidade_retirada = quantidade_retirada
        tanque.data_retirada = data_retirada
        tanque.estado_ativo = False  # Marca como inativo
        tanque.save()

        messages.success(request, f"Tanque {tanque.id_tanque} despovoado com sucesso!")
        return redirect('tanques')

    return redirect('tanques')


#notificacao



@login_required
def notificacoes_view(request):
    grupo_usuario = request.user.groups.first()  # Obtém o grupo do usuário

    # Filtrando notificações apenas do grupo do usuário
    if grupo_usuario:
        notificacoes = Notificacao.objects.filter(grupo=grupo_usuario).order_by('-criada_em')
    else:
        notificacoes = Notificacao.objects.all().order_by('-criada_em')

    # Filtros de categoria e prioridade
    categoria = request.GET.get('categoria', '')  # "tanques" ou "insumos"
    prioridade = request.GET.get('prioridade', '')  # "warning" ou "danger"

    if categoria:
        if categoria == "tanques":
            notificacoes = notificacoes.filter(mensagem__icontains="Tanque")
        elif categoria == "insumos":
            notificacoes = notificacoes.filter(mensagem__icontains="Insumo")

    if prioridade:
        notificacoes = notificacoes.filter(tipo=prioridade)

    return render(request, 'gerenciamento/notificacao/notificacoes.html', {
        'notificacoes': notificacoes,
        'categoria': categoria,
        'prioridade': prioridade
    })





def verificar_notificacoes():
    hoje = now().date()

    # 🧹 REMOVE NOTIFICAÇÕES ANTIGAS antes de adicionar novas (evita duplicação)
    Notificacao.objects.filter(tipo__in=["warning", "danger"]).delete()

    # 🔎 Busca tanques que estão próximos da retirada OU que já passaram da data
    tanques = Tanque.objects.filter(
        previsao_retirada__lte=hoje + timedelta(days=7),
        estado_ativo=True
    )

    for tanque in tanques:
        dias_faltando = (tanque.previsao_retirada - hoje).days

        if dias_faltando < 0:  # ⚠️ Tanque expirado
            mensagem = f" Tanque {tanque.id_tanque} EXPIRADO! Data prevista: {tanque.previsao_retirada.strftime('%d/%m/%Y')}"
            tipo = "danger"
        else:  # 🔔 Aviso para retirada próxima
            dia_text = "dia" if dias_faltando == 1 else "dias"
            mensagem = f" Tanque {tanque.id_tanque} tem previsão de retirada em {dias_faltando} {dia_text}!"
            tipo = "warning"

        # ✅ Agora garantimos que só criamos **uma** notificação nova
        Notificacao.objects.create(
            mensagem=mensagem, 
            tipo=tipo,
            grupo=tanque.grupo  
        )

    # 🔎 Insumos abaixo do estoque mínimo
    insumos = Insumo.objects.filter(quantidade_produto__lte=F('estoque_minimo'))
    for insumo in insumos:
        mensagem = f" Insumo {insumo.nome_produto} está abaixo do estoque mínimo!"
        
        # ✅ Garantimos que só criamos **uma** notificação nova
        Notificacao.objects.create(
            mensagem=mensagem, 
            tipo="danger",
            grupo=insumo.grupo  
        )



def get_notifications(request):
    verificar_notificacoes()
    notificacoes = Notificacao.objects.filter(lida=False).order_by('-criada_em')
    data = {
        "notificacoes": [
            {"id": n.id, "mensagem": n.mensagem, "tipo": n.tipo} for n in notificacoes
        ],
        "count": notificacoes.count()
    }
    return JsonResponse(data)

@login_required
def marcar_notificacoes_como_lidas(request):
    grupo_usuario = request.user.groups.first()
    
    if grupo_usuario:
        Notificacao.objects.filter(grupo=grupo_usuario, lida=False).update(lida=True)
    else:
        Notificacao.objects.filter(lida=False).update(lida=True)

    return JsonResponse({"status": "ok"})


#login

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index") 
    
    error = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")  
        else:
            error = "Usuário ou senha inválidos"

    return render(request, "gerenciamento/login/login.html", {"error": error})

def logout_view(request):
    logout(request)
    return redirect("login")  # Volta para o login ao sair


#view perfil

@login_required
def editar_perfil(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        perfil.nome = request.POST.get("nome", perfil.nome)
        if 'imagem' in request.FILES:
            perfil.imagem = request.FILES['imagem']
        perfil.save()
        return redirect('perfil')  # Redireciona para evitar reenvio do formulário

    return render(request, "gerenciamento/login/perfil.html", {"perfil": perfil})
