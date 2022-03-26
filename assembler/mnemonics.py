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
    # pseudo opcodes
    ORG = -1
    RMB = -2  # Reserve memory byte
    FCB = -3  # Form constant byte
    END = -4


class InstructionType(Enum):
    INHERENT = auto()
    IMMEDIATE_8 = auto()
    IMMEDIATE_16 = auto()
    ABSOLUTE = auto()
    REGISTER_INDIRECT = auto()
    RELATIVE = auto()
    PSEUDO = auto()


Instruction = tuple[Opcode, InstructionType]


_instructions: list[Instruction] = [
    (Opcode.NOP, InstructionType.INHERENT),
    (Opcode.CLRA, InstructionType.INHERENT),
    (Opcode.COMA, InstructionType.INHERENT),
    (Opcode.NEGA, InstructionType.INHERENT),
    (Opcode.LDA_I, InstructionType.IMMEDIATE_8),
    (Opcode.LDAX, InstructionType.REGISTER_INDIRECT),
    (Opcode.LDA, InstructionType.ABSOLUTE),
    (Opcode.STAX, InstructionType.REGISTER_INDIRECT),
    (Opcode.STA, InstructionType.ABSOLUTE),
    (Opcode.ADDA_I, InstructionType.IMMEDIATE_8),
    (Opcode.ADDA, InstructionType.ABSOLUTE),
    (Opcode.ANDA_I, InstructionType.IMMEDIATE_8),
    (Opcode.ANDA, InstructionType.ABSOLUTE),
    (Opcode.CMPA_I, InstructionType.IMMEDIATE_8),
    (Opcode.CMPA, InstructionType.ABSOLUTE),
    (Opcode.LDX_I, InstructionType.IMMEDIATE_16),
    (Opcode.LDX, InstructionType.ABSOLUTE),
    (Opcode.STX, InstructionType.ABSOLUTE),
    (Opcode.CMPX_I, InstructionType.IMMEDIATE_16),
    (Opcode.CMPX, InstructionType.ABSOLUTE),
    (Opcode.ADDX_I, InstructionType.IMMEDIATE_16),
    (Opcode.ADDX, InstructionType.ABSOLUTE),
    (Opcode.LDS_I, InstructionType.IMMEDIATE_16),
    (Opcode.BNE, InstructionType.RELATIVE),
    (Opcode.BEQ, InstructionType.RELATIVE),
    (Opcode.BRA, InstructionType.RELATIVE),
    (Opcode.JMP, InstructionType.ABSOLUTE),
    (Opcode.JSR, InstructionType.ABSOLUTE),
    (Opcode.RTS, InstructionType.INHERENT),
    (Opcode.ORG, InstructionType.PSEUDO),
    (Opcode.END, InstructionType.PSEUDO),
    (Opcode.RMB, InstructionType.PSEUDO),
    (Opcode.FCB, InstructionType.PSEUDO),
]


def createInstructionSet():
    instruction_set: dict[str, Instruction] = dict()

    for instruction in _instructions:
        instruction_set[instruction[0].name] = instruction
    return instruction_set
