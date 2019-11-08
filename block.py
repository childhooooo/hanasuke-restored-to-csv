from enum import Enum, auto
import re


class BlockType(Enum):
    SPACE = auto()
    DIR = auto()
    DIR_L = auto()
    DIR_R = auto()
    CHECK = auto()
    IDENT = auto()
    FILESIZE = auto()
    DATE = auto()
    TIME = auto()


PATTERNS = {
    BlockType.SPACE: re.compile(r'^$'),
    BlockType.DIR: re.compile(r'^\[.+\]$'),
    BlockType.DIR_L: re.compile(r'^\[.+'),
    BlockType.DIR_R: re.compile(r'.+\]$'),
    BlockType.CHECK: re.compile(r'^\(.{1}\)$'),
    BlockType.FILESIZE: re.compile(r'^\d+(\.\d{1,3})??(G|M|K)??B$'),
    BlockType.DATE: re.compile(r'^\d{4}/\d{2}/\d{2}$'),
    BlockType.TIME: re.compile(r'^\d{2}:\d{2}:\d{2}')
}


def classify_block(block):
    for key, pattern in PATTERNS.items():
        if pattern.match(block):
            return key
    return BlockType.IDENT
