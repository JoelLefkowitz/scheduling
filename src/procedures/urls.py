from django.urls import path

from .views import ProcedureIngestView

urlpatterns = [
    path("ingest/", ProcedureIngestView.as_view(), name="ingest"),
]
