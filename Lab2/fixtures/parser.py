import re

REGEXP = '\[\s*[0-9]*\]\s*[0-9\.-]*\s*(sec)\s*[0-9\.]*\s*[A-Z]?(Bytes)\s*[0-9\.]*\s*[A-Z]?(bits/sec)\s*[0-9]*\s*[0-9\.]*\s*[A-Z]?(Bytes)'
KEYS = ('Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd')


def is_correct_string(string):
    return re.match(REGEXP, string) is not None


def get_correct_lines(lines):
    correct_lines = []
    for string in lines:
        if is_correct_string(string):
            correct_lines.append(string)
    return correct_lines


def parse_line(line):
    line = line[line.index(']') + 1:]
    line = re.sub(r'[A-Z]?(bits/sec)', '', line)
    line = re.sub(r'[A-Z]?(Bytes)', '', line)
    line = re.sub(r'(sec)', '', line)
    values = list(filter(lambda x: bool(x), line.split(' ')))
    result = {key: value for key, value in zip(KEYS, values)}
    for key in result:
        if key != 'Interval':
            result[key] = float(result[key])
    return result


def parser(text):
    lines = get_correct_lines(text.split('\n'))
    result = [parse_line(line) for line in lines]
    return result


