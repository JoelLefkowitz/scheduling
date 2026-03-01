import pytest
from rest_framework.exceptions import ParseError

from services.payloads.procedures import PatientPayload, ProcedurePayload


def test_parse_valid() -> None:
    parsed = ProcedurePayload.parse(
        "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
        "SCH|A1001|PROC123|20250102|093000|120000\n"
        "PID|123456|DOE^JOHN"
    )

    patient = PatientPayload(
        patient_id="123456",
        first_name="JOHN",
        last_name="DOE",
    )

    procedure = ProcedurePayload(
        schedule_id="A1001",
        procedure_code="PROC123",
        procedure_date="20250102",
        start_time="093000",
        end_time="120000",
        patient=patient,
    )

    assert parsed == procedure


@pytest.mark.parametrize(
    "body,error",
    [
        (
            "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
            "SCH|A1001|PROC123|20250102|093000|120000",
            "Expected 3 HL7 segments",
        ),
        (
            "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
            "SCH|A1001|PROC123|20250102|093000\n"
            "PID|123456|DOE^JOHN",
            "Expected 6 SCH fields",
        ),
        (
            "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
            "SCH|A1001|PROC123|20250102|093000|120000\n"
            "PID|123456",
            "Expected 3 PID fields",
        ),
        (
            "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
            "SCH|A1001|PROC123|20250102|093000|120000\n"
            "PID|123456|DOE",
            "Expected 2 patient name components",
        ),
    ],
)
def test_parse_invalid(body: str, error: str) -> None:
    with pytest.raises(ParseError, match=error):
        ProcedurePayload.parse(body)
