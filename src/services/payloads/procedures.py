from dataclasses import dataclass

from rest_framework.exceptions import ParseError

from .patients import PatientPayload


@dataclass(frozen=True)
class ProcedurePayload:
    schedule_id: str
    procedure_code: str
    procedure_date: str
    start_time: str
    end_time: str
    patient: PatientPayload

    @classmethod
    def parse(cls, text: str) -> ProcedurePayload:
        """
        Parse an HL7 procedure scheduling message into a ProcedurePayload.

        Raises:
            ParseError: If the message structure is malformed.
        """
        segments = text.split("\n")

        if len(segments) != 3:
            raise ParseError("Expected 3 HL7 segments")

        sch = segments[1].split("|")

        if len(sch) != 6:
            raise ParseError("Expected 6 SCH fields")

        pid = segments[2].split("|")

        if len(pid) != 3:
            raise ParseError("Expected 3 PID fields")

        name = pid[2].split("^")

        if len(name) != 2:
            raise ParseError("Expected 2 patient name components")

        patient = PatientPayload(
            patient_id=pid[1],
            first_name=name[1],
            last_name=name[0],
        )

        return cls(
            schedule_id=sch[1],
            procedure_code=sch[2],
            procedure_date=sch[3],
            start_time=sch[4],
            end_time=sch[5],
            patient=patient,
        )
