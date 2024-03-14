from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, ListView
from xhtml2pdf import pisa
from django.db.models import Count
from django.db.models.functions import *
from django.db.models import Count, F
from django.template.loader import render_to_string

from core import models
from core.models import Paciente, Convenio, Consulta, Medico


class HomeTemplateView(TemplateView):
    template_name = "index.html"


class PacientesListView(ListView):
    template_name = "relatorios/pacientes.html"
    model = Paciente
    context_object_name = 'pacientes'


class RelatPdfPacientes(View):

    def get(self, request):
        pacientes = Paciente.objects.all()
        data = {
            'pacientes': pacientes,
        }
        template = get_template("relatorios/pdfpacientes.html")
        html = template.render(data)
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            return HttpResponse(result.getvalue(),
                                content_type='application/pdf')
        except Exception as e:
            print(e)
            return None


class PacientesConvenioListView(ListView):
    template_name = 'relatorios/pacientes_por_convenio.html'
    model = Convenio
    context_object_name = 'convenios'

    def get_queryset(self):
        convenios = Convenio.objects.all()
        for convenio in convenios:
            pacientes = Paciente.objects.filter(possui__convenio=convenio)
            convenio.pacientes = pacientes
        return PacientesConvenioListView


class RelatPdfPacientesPorConvenio(View):

    def get(self, request):
        convenios = Convenio.objects.all()
        for convenio in convenios:
            pacientes = Paciente.objects.filter(possui__convenio=convenio)
            convenio.pacientes = pacientes

        data = {
            'convenios': convenios,
            'pacientes': pacientes,
        }

        template = get_template("relatorios/pdfpacientes_por_convenio.html")
        html = template.render(data)
        response = HttpResponse(content_type='application/pdf')

        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            response.write(result.getvalue())
            return response
        except Exception as e:
            print(e)
            return response


class ConsultaPorEspecialidadeListView(ListView):
    template_name = "relatorios/consulta_por_especialidade.html"
    model = Consulta
    context_object_name = 'Consulta por especialidade'
    queryset = Convenio.objects.all()


class RelatpdfConsultaPorEspecialidade(View):

    def get(self, request):
        consulta = Consulta.objects.all()
        data = {
            'Consulta': Consulta,
        }
        template = get_template("relatorios/pdfconsulta_por_especialidade.html")
        html = template.render(data)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return RelatpdfConsultaPorEspecialidade


class AtendimentoEspecialidadeListView(ListView):
    template_name = 'relatorios/atendimento_por_especialidade.html'
    context_object_name = 'atendimento_por_especialidade'

    def get_queryset(self):
        especialidades = Medico.objects.values_list('especialidade', flat=True).distinct()

        atendimentos_por_especialidade = []
        print(especialidades)
        for especialidade in especialidades:
            atendimentos = Consulta.objects.filter(medico__especialidade=especialidade).annotate(
                month=ExtractMonth('data'),
                year=ExtractYear('data')) \
                .values('month', 'year') \
                .annotate(total=Count('id'))
            atendimentos_por_especialidade.append({'especialidade': especialidade, 'atendimentos': atendimentos})

        return atendimentos_por_especialidade


class RelatPdfAtendimentoEspecialidadeListView(View):

    def get(self, request):
        atendimento_por_especialidade = AtendimentoEspecialidadeListView().get_queryset()
        print(atendimento_por_especialidade)
        html_string = render_to_string('relatorios/pdfatendimento_por_especialidade.html',
                                       {'atendimento_por_especialidade': atendimento_por_especialidade})

        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            return response

        return HttpResponse('Erro ao gerar PDF: %s' % pdf.err)