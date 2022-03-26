from io import TextIOWrapper

from assembler.mnemonics import InstructionType, Opcode, createInstructionSet
from assembler.tokenizer import TokenType, tokenizer

MAX_RMB = 0x8000  # Max number of bytes to reserve

BAD_DIRECTIVE = "Invalid directive"
BAD_MNEMONIC = "Invalid mnemonic"
BAD_OPERAND = "Operand is invalid"
BAD_REGISTER = "Invalid register"
COMMA_EXPECTED = "Expected a ','"
EXTRA_GARBAGE = "Symbol is unexpected"
NUMBER_EXPECTED = "Expected a number"
OUT_OF_RANGE = "Number is out of range"
STORE_OVERFLOW = "Program exceeds available memory"
SYNTAX_ERROR = "Syntax error"
UNDEFINED_OPERAND = "Operand is undefined"
MNEMONIC_EXPECTED = "Mnemonic expected"
UNDEFINED_MNEMONIC = "Undefined mnemonic"
UNDEFINED_LABEL = "Undefined label"
OPERAND_EXPECTED = "Operand expected"
LOCATION_EXPECTED = "Location expected"


class AsmError(Exception):
    def __init__(self, reason, pos, line):
        pointer = (" " * pos) + "^"
        self.message = f"{reason}:\n{line.rstrip()}\n{pointer}"
        super().__init__(self.message)


END_OF_STATEMENT_TOKENS = TokenType.COMMENT, TokenType.EOL
OPERANDLESS_INSTRUCTION_TYPES = (
    InstructionType.INHERENT,
    InstructionType.REGISTER_INDIRECT,
)


def assemble(file: TextIOWrapper):
    org = 0
    start = 0
    binary_code: list[int] = []
    symbol_table = dict()
    instruction_set = createInstructionSet()

    def _get_symbol_table_value(key):
        try:
            return symbol_table[key]
        except KeyError:
            return None

    for _pass in range(1, 3):
        file.seek(0)
        binary_code.clear()

        for line in file:
            # skip blank lines
            if line.strip() == "":
                continue

            tokens = tokenizer(line)
            token = next(tokens)

            operand = 0
            if token.type is TokenType.NAME:
                if _pass == 1:
                    symbol_table[token.text] = len(binary_code) + org
                token = next(tokens)
            if token.type is not TokenType.WHITESPACE:
                # mnemonics must be indented
                raise AsmError(SYNTAX_ERROR, token.pos, line)
            token = next(tokens)
            if token.type is not TokenType.NAME:
                raise AsmError(MNEMONIC_EXPECTED, token.pos, line)
            mnemonic_pos = token.pos
            mnemonic = token.text.upper()
            try:
                instruction = instruction_set[mnemonic]
            except KeyError as exc:
                raise AsmError(UNDEFINED_MNEMONIC, mnemonic_pos, line) from exc
            opcode, instruction_type = instruction

            if instruction_type in OPERANDLESS_INSTRUCTION_TYPES:
                binary_code.append(opcode.value)
            elif instruction_type is InstructionType.ABSOLUTE:
                token = next(tokens)
                if token.type is TokenType.WHITESPACE:
                    token = next(tokens)
                if token.type is TokenType.HASH:
                    # Immediate instruction
                    mnemonic += "_I"
                    token = next(tokens)
                    instruction = instruction_set[mnemonic]
                    if instruction is None:
                        raise AsmError(UNDEFINED_MNEMONIC, mnemonic_pos, line)
                    opcode, instruction_type = instruction
                    if token.type is not TokenType.NUMBER:
                        raise AsmError(NUMBER_EXPECTED, token.pos, line)
                    operand = token.value
                    binary_code.append(opcode.value)
                    binary_code.append(operand & 0xFF)
                    if instruction_type is InstructionType.IMMEDIATE_16:
                        binary_code.append((operand & 0xFF00) >> 8)
                elif token.type is TokenType.NAME:
                    if _pass == 2:
                        operand = _get_symbol_table_value(token.text)
                        if not operand:
                            raise AsmError(UNDEFINED_LABEL, token.pos, line)
                    binary_code.append(opcode.value)
                    binary_code.append(operand & 0xFF)
                    binary_code.append((operand & 0xFF00) >> 8)
            elif instruction_type is InstructionType.RELATIVE:
                offset = 0
                token = next(tokens)
                if token.type is TokenType.WHITESPACE:
                    token = next(tokens)
                if token.type is TokenType.NAME:
                    if _pass == 2:
                        address = _get_symbol_table_value(token.text)
                        if not address:
                            raise AsmError(UNDEFINED_LABEL, token.pos, line)
                        offset = address - len(binary_code)
                else:
                    raise AsmError(OPERAND_EXPECTED, token.pos, line)
                if -127 <= offset <= 127:
                    binary_code.append(opcode.value)
                    binary_code.append(offset)
                else:
                    raise AsmError(OUT_OF_RANGE, token.pos, line)
            elif instruction_type is InstructionType.PSEUDO:
                if opcode is Opcode.ORG:
                    token = next(tokens)
                    if token.type is TokenType.WHITESPACE:
                        token = next(tokens)
                    if token.type is not TokenType.NUMBER:
                        raise AsmError(NUMBER_EXPECTED, token.pos, line)
                    org = token.value
                elif opcode is Opcode.END:
                    token = next(tokens)
                    if token.type is TokenType.WHITESPACE:
                        token = next(tokens)
                    if token.type is not TokenType.NAME:
                        raise AsmError(LOCATION_EXPECTED, token.pos, line)
                    if _pass == 2:
                        start = _get_symbol_table_value(token.text)
                        if not start:
                            AsmError(UNDEFINED_LABEL, token.pos, line)
                elif opcode is Opcode.RMB:
                    token = next(tokens)
                    if token.type is TokenType.WHITESPACE:
                        token = next(tokens)
                    if token.type is not TokenType.NUMBER:
                        raise AsmError(NUMBER_EXPECTED, token.pos, line)
                    if 0 < token.value <= MAX_RMB:
                        binary_code.extend([0] * token.value)
                    else:
                        raise AsmError(OUT_OF_RANGE, token.pos, line)
                elif opcode is Opcode.FCB:
                    token = next(tokens)
                    if token.type is TokenType.WHITESPACE:
                        token = next(tokens)
                    if token.type is not TokenType.NUMBER:
                        raise AsmError(NUMBER_EXPECTED, token.pos, line)
                    binary_code.append(token.value & 0xFF)
                else:
                    raise AsmError(BAD_MNEMONIC, token.pos, line)
            else:
                raise Exception("Logic error")

            token = next(tokens)
            if token.type is not TokenType.WHITESPACE:
                raise AsmError(SYNTAX_ERROR, token.pos, line)

    return binary_code, org, start
