import re
from enum import Enum
from block import BlockType, classify_block


class Parser(object):

    def __init__(self):
        self.init()

    def init(self):
        self.beginning = False
        self.indent = 0
        self.results = {
            BlockType.DIR: None,
            BlockType.DIR_L: None,
            BlockType.DIR_R: None,
            BlockType.CHECK: None,
            BlockType.FILESIZE: None,
            BlockType.DATE: None,
            BlockType.TIME: None
        }

    def parse(self, line):
        self.init()
        blocks = re.split(r'[ \n]', line)
        for index, block in enumerate(blocks):
            block_type = classify_block(block)

            if block_type != BlockType.SPACE:
                self.beginning = True
                self.results[block_type] = {
                    'position': index,
                    'value': block
                }

            if not self.beginning:
                self.indent += 1

        return blocks

    def get_dir(self):
        return {
            'dir': self.results[BlockType.DIR]['value'].strip('[').strip(']'),
            'indent': self.indent
        }

    def build_dir(self, blocks):
        begin = self.results[BlockType.DIR_L]['position']
        end = self.results[BlockType.DIR_R]['position']
        return {
            'dir': ' '.join(blocks[begin:end+1]).strip('[').strip(']'),
            'indent': self.indent
        }

    def build_info(self, blocks):
        try:
            begin = self.results[BlockType.CHECK]['position']
            check = self.results[BlockType.CHECK]['value']
        except:
            begin = 0
            check = '()'
        end = self.results[BlockType.FILESIZE]['position']
        filenames = blocks[begin+1:end]
        filename = ' '.join(filenames).strip()
        return {
            'filename': filename,
            'check': check,
            'filesize': self.results[BlockType.FILESIZE]['value'],
            'date': self.results[BlockType.DATE]['value'],
            'time': self.results[BlockType.TIME]['value']
        }

