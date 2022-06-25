from enum import Enum, auto


# cspell: disable
class Opcode(Enum):
    NOP = 0x12
    CLRA = 0x4F
    COMA = 0x43
    NEGA = 0x40
    LDA_I = 0x86
    LDAX = 0xA6
    LDA = 0xB6
    STAX = 0xA7
    STA = 0xB7
    ADDA_I = 0x8B
    ADDA = 0xBB
    ANDA_I = 0x84
    ANDA = 0xB4
    CMPA_I = 0x81
    CMPA = 0xB1
    LDX_I = 0x8E
    LDX = 0xBE
    STX = 0xBF
    CMPX_I = 0x8C
    CMPX = 0xBC
    ADDX_I = 0x30
    ADDX = 0x31
    LDS_I = 0x8F
    BNE = 0x26
    BEQ = 0x27
    BRA = 0x20
    JMP = 0x7E
    JSR = 0xBD
    RTS = 0x39


class InstructionType(Enum):
    INHERENT = auto()
    IMMEDIATE = auto()
    ABSOLUTE = auto()
    REGISTER_INDIRECT = auto()
    RELATIVE = auto()
