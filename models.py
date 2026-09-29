# not used yet, just a placeholder for later
from dataclasses import dataclass

@dataclass
class Expense:
    id: int
    amt: float
    cat: str
    desc: str
    dt: str

@dataclass
class Budget:
    id: int
    cat: str
    lim: float
