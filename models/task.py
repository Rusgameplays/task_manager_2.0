from dataclasses import dataclass


@dataclass
class Task:
    rf: str
    sd: str

    name: str
    full_name: str

    type: str
    mp8: str
    secure: str

    status: str
    pentest_audit: str
    compliance: str

    comment: str

    folder_id: str