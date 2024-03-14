from django.urls import path

from core import views

from django.urls import path

from core import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('relatorios/pacientes', views.PacientesListView.as_view(), name='relat_pacientes'),
    path('relatorios/pdfpacientes', views.RelatPdfPacientes.as_view(), name='pdf_pacientes'),

    path('relatorios/pacientes_por_convenio', views.PacientesConvenioListView.as_view(),
         name='pacientesporconvenio'),
    path('relatorios/pdfpacientes_por_convenio', views.RelatPdfPacientesPorConvenio.as_view(),
         name='RelatPdfPacientesPorConvenio'),

    path('relatorios/consulta_por_especialidade', views.ConsultaPorEspecialidadeListView.as_view(),
         name='consulta_por_especialidade'),
    path('relatorios/pdfconsulta_por_especialidade', views.RelatpdfConsultaPorEspecialidade.as_view(),
         name='pdfconsulta_por_especialidade'),

    path("relatorios/atendimento_por_especialidade", views.AtendimentoEspecialidadeListView.as_view(),
        name="relat_atendimento_por_especialidade"),
        path("relatorios/pdf/pdfatendimento_por_especialidade", views.RelatPdfAtendimentoEspecialidadeListView.as_view(),
        name="pdfatendimento_por_especialidade"),

]

