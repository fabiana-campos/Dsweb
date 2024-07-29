from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Pergunta, Alternativa
from django.views import View #importandoSuperClasseView

class IndexView(View):
    def get(self, request, *args, **kwargs):
        enquetes = Pergunta.objects.order_by('-pub_date')[:10]
        contexto = {'lista_enquetes': enquetes}
        return render(request, 'enquetes/index.html', contexto)

class DetalhesView(View):
    def get(self, request, *args, **kwargs):
        pergunta_id = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
        contexto = {'enquete': pergunta}
        return render(request, 'enquetes/detalhes.html', contexto)

    def post(self, request, *args, **kwargs):
        pergunta_id = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
        try:
            id_alternativa = request.POST['escolha']
            alt = pergunta.alternativa_set.get(pk=id_alternativa)
        except (KeyError, Alternativa.DoesNotExist):
            contexto = {
                'enquete': pergunta,
                'error': 'Você precisa selecionar uma alternativa.'
            }
            return render(request, 'enquetes/detalhes.html', contexto)
        else:
            alt.quant_votos += 1
            alt.save()
            return HttpResponseRedirect(reverse('enquetes:resultado', args=(pergunta.id,)))


class ResultadoView(View):
    def get(self, request, *args, **kwargs):
        pergunta_id = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
        contexto = {'enquete': pergunta}
        return render(request, 'enquetes/resultado.html', contexto)

####
## Histórico
"""
--> View INDEX - Versão 1
def index(request):
    lista = Pergunta.objects.all()
    template = loader.get_template('enquetes/index.html')
    contexto = {'lista_enquetes': lista}
    return HttpResponse(template.render(contexto, request))

    View INDEX versão 2
    def index(request):
    enquetes = Pergunta.objects.order_by('-pub_date')[:10]
    contexto = {'lista_enquetes': enquetes}
    return render(request, 'enquetes/index.html', contexto)

    View INDEX versão 3
    class IndexView(generic.ListView):
        template_name = 'enquetes/index.html'
        def get_queryset(self):
            return Pergunta.objects.order_by('-pub_date')[:10]


--> View - Detalhes - Versão 1
def detalhes(request, pergunta_id):
    resultado = 'DETALHES da enquete de número %s'
    return HttpResponse(resultado % pergunta_id)

--> View - DETALHES - versão 2
def detalhes(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
    contexto = {'enquete': pergunta}
    return render(request, 'enquetes/detalhes.html', contexto)

--> View Detalhes -versão 3:
class DetalhesView(View):
    model = Pergunta


--> VIEW RESULTADO - VERSÃO 1
def resultado(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
    contexto = {'enquete': pergunta}
    return render(request, 'enquetes/resultado.html', contexto)

--> VIEW RESULTADO - VERSÃO 2
class ResultadoView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/resultado.html'

--> View VOTAÇÃO - versão 1
def votacao(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        id_alternativa = request.POST['escolha']
        alt = pergunta.alternativa_set.get(pk=id_alternativa)
    except (KeyError, Alternativa.DoesNotExist):
        contexto = {
            'enquete': pergunta,
            'error': 'Você precisa selecionar uma alternativa.'
        }
        return render(request, 'enquetes/detalhes.html', contexto)
    else:
        alt.quant_votos += 1
        alt.save()
        return HttpResponseRedirect(reverse('enquetes:resultado', args=(pergunta.id,)))
"""