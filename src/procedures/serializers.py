from rest_framework import serializers

from .models import Patient, Procedure


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "patient_id",
            "first_name",
            "last_name",
        ]

        extra_kwargs = {
            "patient_id": {
                "validators": [],
            },
        }


class ProcedureSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Procedure
        fields = [
            "id",
            "schedule_id",
            "procedure_code",
            "procedure_date",
            "start_time",
            "end_time",
            "patient",
        ]

    def create(self, validated_data):
        """
        Create a procedure and the patient if it doesnt exist.
        """
        patient_data = validated_data.pop("patient")
        patient_id = patient_data.pop("patient_id")

        patient, _ = Patient.objects.get_or_create(
            patient_id=patient_id,
            defaults=patient_data,
        )

        procedure = Procedure.objects.create(
            patient=patient,
            **validated_data,
        )

        return procedure
