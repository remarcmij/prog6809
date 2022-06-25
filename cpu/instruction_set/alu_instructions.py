from dataclasses import dataclass


@dataclass
class ALUState:
    A: int
    X: int
    Z: int
