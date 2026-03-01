from dataclasses import dataclass


@dataclass(frozen=True)
class PatientPayload:
    patient_id: str
    first_name: str
    last_name: str
