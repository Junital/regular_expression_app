import argparse
import os
import re

# TERMINAL COLOR

RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

# DEFINITION

parser = argparse.ArgumentParser(prog="Regular Expression App", description='Search with your regular expression pattern.')

parser.add_argument('pattern', type=str, help='pattern for searching', metavar="P")

parser.add_argument('--config', type=str, required=False, help="locate the directory (default: current directory), you just need to config it once")

parser.add_argument('-r', type=bool, required=False, help="recursive search or not", default=False)

parser.add_argument('--version', action='version', version='%(prog)s 0.0.2')

# CONFIG HANDLE

current_dir = os.getcwd()

script_dir = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(script_dir, *['config', 'config.conf'])

setting = {}

try:
    os.access(config_file, os.R_OK)

    with open(config_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.strip() != '':
            keyword, value = line.split('=')
            setting[keyword] = value.rstrip('\n')

except OSError:
    os.makedirs(os.path.dirname(config_file), exist_ok=True)

    with open(config_file, 'w') as f:
        f.write("directory=" + str(current_dir) + '\n')
    setting["directory"] = str(current_dir)

args = parser.parse_args()

if(args.config):
    setting["directory"] = str(args.config)


# SEARCH PATTERN
if(args.pattern):
    # print(args.pattern)
    # print(setting["directory"])

    results = []
    pattern = re.compile(r'{}'.format(args.pattern), re.IGNORECASE)

    for root, _, files in os.walk(setting["directory"]):
        # print(files)
        # print(root)
        # print(1)
        for file in files:
            file_path = os.path.join(root, file)
            # print(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.finditer(content)
                    for match in matches:
                        context_start = max(0, match.start() - 30)
                        context_end = min(len(content), match.end() + 30)
                        context = content[context_start:context_end]
                        results.append((file_path, context))
            except UnicodeDecodeError:
                # print(f'{BOLD}{RED}{"File:"}{RESET} {RED}{file_path} is not a searchable file.\n{RESET}')
                pass
    # print(results)

    if results:
        for result in results:
            pieces = [(match.start(), match.end()) for match in pattern.finditer(result[1])]

            parts = []
            prev_index = 0

            for piece in pieces:
                parts.append(result[1][prev_index:piece[0]])
                parts.append(result[1][piece[0]:piece[1]])
                prev_index = piece[1]
            parts.append(result[1][prev_index:])

            print(f'{BOLD}{GREEN}{"File:"}{RESET} {GREEN}{result[0]}\n{RESET}')
            print(f'{BOLD}{"Context:"}{RESET}', end=' ')
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    print(f'{part}', end='')
                else:
                    print(f'{YELLOW}{part}{RESET}', end='')
            print('\n')

# SAVE CONFIG FILE

os.remove(config_file)

with open(config_file, 'w') as f:
    for set in setting:
        f.write(str(set) + "=" + str(setting[set]))
        f.write("\n")

