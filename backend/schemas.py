
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class LoanInput(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    person_age: int = Field(gt=0, le=100)

    person_income: float = Field(gt=0)

    person_home_ownership: str

    person_emp_length: Optional[float] = Field(
        default=None,
        ge=0
    )

    loan_intent: str

    loan_grade: str

    loan_amnt: float = Field(gt=0)

    loan_int_rate: Optional[float] = Field(
        default=None,
        ge=0
    )

    loan_percent_income: float = Field(ge=0)

    cb_person_default_on_file: str

    cb_person_cred_hist_length: float = Field(ge=0)
