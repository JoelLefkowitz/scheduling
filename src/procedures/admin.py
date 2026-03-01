from django.contrib import admin

from .models import Patient, Procedure


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "first_name",
        "last_name",
    )
    search_fields = (
        "patient_id",
        "first_name",
        "last_name",
    )


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = (
        "schedule_id",
        "procedure_code",
        "procedure_date",
        "start_time",
        "end_time",
        "patient",
    )

    search_fields = (
        "schedule_id",
        "procedure_code",
        "patient__patient_id",
    )
