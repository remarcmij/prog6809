import re
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    COMMA = auto()
    COMMENT = auto()
    DIRECTIVE = auto()
    EOL = auto()
    LABEL = auto()
    LOCATION = auto()
    MINUS = ()
    NAME = auto()
    NUMBER = auto()
    PLUS = ()
    REGISTER = auto()
    WHITESPACE = auto()
    OTHER = auto()
    HASH = auto()
    HEXADECIMAL = auto()


@dataclass
class Token:
    type: TokenType
    text: str
    pos: int
    value: int


token_patterns = [
    (TokenType.NAME, re.compile(r"([A-Z]\w*)", re.IGNORECASE)),
    (TokenType.HEXADECIMAL, re.compile(r"([0-9][0-9A-F]+)H", re.IGNORECASE)),
    (TokenType.NUMBER, re.compile(r"([-+]?\d+)")),
    (TokenType.COMMA, re.compile(r"(,)")),
    (TokenType.PLUS, re.compile(r"(\+)")),
    (TokenType.MINUS, re.compile(r"(-)")),
    (TokenType.HASH, re.compile(r"(#)")),
    (TokenType.COMMENT, re.compile(r"(\s*;)")),
    (TokenType.WHITESPACE, re.compile(r"(\s+)")),
    (TokenType.OTHER, re.compile(r"(.)")),
]


def tokenizer(line: str):
    start = 0
    stop = len(line)
    while start < stop:
        for _type, pattern in token_patterns:
            match = pattern.match(line, start)
            if match:
                text = match.group(1).upper()
                value = 0
                if _type == TokenType.NUMBER:
                    value = int(text)
                elif _type == TokenType.HEXADECIMAL:
                    value = int(text, 16)
                    _type = TokenType.NUMBER
                yield Token(_type, text, start, value)
                start = match.end()
                break
        else:
            raise Exception("Logic error in tokenizer")
    yield Token(TokenType.EOL, "", 0, 0)
