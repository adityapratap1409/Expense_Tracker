from dataclasses import dataclass
from typing import Optional

# domain models
@dataclass
class Expense:
    id: Optional[int]
    amt: float
    cat: str
    desc: str
    dt: str

@dataclass
class Budget:
    id: Optional[int]
    cat: str
    lim: float
