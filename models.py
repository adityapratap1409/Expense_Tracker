# simple dataclasses, handy if we want typed objects instead of raw sqlite rows later
from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    id: Optional[int]
    amt: float
    cat: str
    desc: str
    dt: str  # YYYY-MM-DD


@dataclass
class Budget:
    id: Optional[int]
    cat: str
    lim: float
