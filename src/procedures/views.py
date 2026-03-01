from dataclasses import asdict

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from services.payloads.procedures import ProcedurePayload

from .serializers import ProcedureSerializer


class ProcedureIngestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Ingest and persist an HL7 procedure scheduling message.

        Returns:
            Response: created procedure and nested patient data
        """
        body = request.body.decode("utf-8")
        parsed = ProcedurePayload.parse(body)

        serializer = ProcedureSerializer(data=asdict(parsed))
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
