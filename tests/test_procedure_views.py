import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_post_valid() -> None:
    body = (
        "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
        "SCH|A1001|PROC123|20250102|093000|120000\n"
        "PID|123456|DOE^JOHN"
    )

    response = APIClient().post("/ingest/", content_type="text/plain", data=body)
    assert response.status_code == HTTP_201_CREATED

    procedure = response.json()
    assert procedure["schedule_id"] == "A1001"
    assert procedure["procedure_code"] == "PROC123"
    assert procedure["procedure_date"] == "2025-01-02"
    assert procedure["start_time"] == "09:30:00"
    assert procedure["end_time"] == "12:00:00"

    patient = procedure["patient"]
    assert patient["patient_id"] == "123456"
    assert patient["first_name"] == "JOHN"
    assert patient["last_name"] == "DOE"


@pytest.mark.parametrize(
    "body,error",
    [
        (
            "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
            "SCH|A1001|PROC123|20250102|093000|120000\n",
            {
                "code": "parse_error",
                "detail": "Expected 3 PID fields",
                "attr": None,
            },
        ),
        (
            "MSH|^~\\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S\n"
            "SCH|A1001|PROC123|20250102|093000|999999\n"
            "PID|123456|DOE^JOHN",
            {
                "code": "invalid",
                "detail": "Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].",
                "attr": "end_time",
            },
        ),
    ],
)
def test_post_invalid(body: str, error: str) -> None:
    response = APIClient().post("/ingest/", content_type="text/plain", data=body)
    assert response.status_code == HTTP_400_BAD_REQUEST

    feedback = response.json()
    assert feedback["errors"] == [error]
