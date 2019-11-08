import os
import sys
import csv
from parser import Parser
from block import BlockType


TAB = 4
LOG_FILE = 'log/log.txt'


def write_line(output, dirs, info):
    with open(output, 'a') as f:
        writer = csv.writer(f)
        path = os.path.join(*dirs)
        writer.writerow([path, info['filename'], info['check'], info['filesize'], info['date'], info['time']])


def write_log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(message)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit(1)

    target = sys.argv[1]
    output = os.path.join('output', os.path.basename(target) + '.csv')
    parser = Parser()

    with open(target, 'r') as f:
        data = f.readlines()

    stack_dir = [] # 取りあえず...
    total = len(data)
    for index, d in enumerate(data):
        print('\r', str(index) + '/' + str(total), sep='', end='')
        blocks = parser.parse(d)

        if parser.results[BlockType.DIR]:
            directory = parser.get_dir()
            depth = directory['indent'] / TAB
            stack_dir = stack_dir[:int(depth)] + [directory['dir']]

        elif parser.results[BlockType.DIR_L] and parser.results[BlockType.DIR_R]:
            directory = parser.build_dir(blocks)
            depth = directory['indent'] / TAB
            stack_dir = stack_dir[:int(depth)] + [directory['dir']]

        else:
            try:
                write_line(output, stack_dir, parser.build_info(blocks))
            except:
                write_log('Line' + str(index))
                write_log(d)
                print("ERROR: Couldn't read parameters from line " + str(index))

    sys.exit(0)
