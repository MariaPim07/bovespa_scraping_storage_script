from pydantic import BaseModel

class BovespaModel(BaseModel):
    sector: str = None
    code: str = None
    stock: str = None
    type: str = None
    theoritical_amount: int = None
    percentage_share: float = None
    percentage_accumulated: float = None