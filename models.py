from pydantic import BaseModel, validator


class AllTransactionCO2(BaseModel):
    co2_value: float
    stamp: str

    @validator('stamp')
    def stamp_validator(cls, v):
        d_list = str(v).split(".")
        valid = True
        if len(d_list) != 3:
            valid = False
        else:
            for d_test in d_list:
                try:
                    float(d_test)
                except Exception as e:
                    valid = False
                    break
        if valid:
            return str(v)
        raise ValueError("Date format must be dd.mm.yy")
