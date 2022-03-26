# import pytest

from io import StringIO
from assembler.assembler import assemble

# cspell: disable


def run_assembler(text: str):
    file_in = StringIO(text)
    return assemble(file_in)


def test_inherent_addressing():
    source = """
    NOP     comment
"""
    result, *_ = run_assembler(source)
    assert result == [
        0x12,  # NOP
    ]


def test_immediate_addressing():
    source = """
    LDA     #10     comment
    LDX     #1234H
"""
    result, *_ = run_assembler(source)
    assert result == [0x86, 0x0A, 0x8E, 0x34, 0x12]


def test_absolute_addressing():
    source = """
        STA     PROD
PROD    RMB     1        Storage for PROD
"""
    result, *_ = run_assembler(source)
    assert result == [
        0xB7,  # STA
        3,  # addr low byte
        0,  # addr high byte
        0,  # RMB 1 @ address 3
    ]


def test_register_indirect_addressing():
    source = """
    LDAX    comment
"""
    result, *_ = run_assembler(source)
    assert result == [
        0xA6,
    ]


def test_relative_addressing():
    source = """
    BRA      LOC
LOC NOP
    """
    result, *_ = run_assembler(source)
    assert result == [0x20, 0x02, 0x12]


def test_FCB():
    source = """
    FCB 12H
    """
    result, *_ = run_assembler(source)
    assert result == [0x12]


def test_ORG_END():
    source = """
        ORG     1234H
START   CLRA
        END START
    """
    result, org, start = run_assembler(source)
    assert result == [0x4F]
    assert org == 0x1234
    assert start == 0x1234
