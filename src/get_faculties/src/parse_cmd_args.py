import argparse

# Setting cli arguments
parser = argparse.ArgumentParser(description='Get courses.')
parser.add_argument('-s', '--struct', dest='structureId', type=int, nargs='?', help='Structure ID')

def parse_cmd_args():
    'Get command line arguments'

    args = parser.parse_args()
    return vars(args)
