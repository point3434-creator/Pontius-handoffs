"""Attribute the journal row of one invocation, or record its absence explicitly.

Usage: journal_attribution.py <journal> <rows_before> <expected_commit> <root> <out>

Prints one line and exits:
  BOUND <output> <output_sha256>   exactly one new row; it names the expected source commit
                                   and its result file exists under <root> with that digest;
                                   the row is copied to <out> (LF).                exit 0
  ABSENT <rows>                    no new row appeared; nothing is written.         exit 3
  EXTRA <rows>                     more than one new row appeared; nothing written. exit 4
  MISMATCH <reason>                one new row that does not bind this attempt.     exit 5
The caller must never substitute an older row for a missing one.
"""
import hashlib
import json
import pathlib
import sys


def main(argv):
    journal, rows_before, commit, root, out = argv[1:6]
    rows_before = int(rows_before)
    root = pathlib.Path(root)
    lines = pathlib.Path(journal).read_bytes().split(b'\n')
    if lines and lines[-1] == b'':
        lines.pop()
    if len(lines) == rows_before:
        print('ABSENT', len(lines))
        return 3
    if len(lines) != rows_before + 1:
        print('EXTRA', len(lines))
        return 4
    raw = lines[-1].rstrip(b'\r')
    try:
        row = json.loads(raw)
    except ValueError as error:
        print('MISMATCH unparsable-row', type(error).__name__)
        return 5
    if row.get('source_commit') != commit:
        print('MISMATCH source_commit', row.get('source_commit'))
        return 5
    output = row.get('output')
    if type(output) is not str or not output:
        print('MISMATCH output-missing')
        return 5
    path = root / output
    if not path.is_file():
        print('MISMATCH output-file-missing', output)
        return 5
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != row.get('output_sha256'):
        print('MISMATCH output_sha256', output)
        return 5
    runtimes = path.parent / 'runtimes.json'
    if 'runtimes_sha256' in row and (not runtimes.is_file() or hashlib.sha256(
            runtimes.read_bytes()).hexdigest() != row['runtimes_sha256']):
        print('MISMATCH runtimes_sha256', output)
        return 5
    pathlib.Path(out).write_bytes(raw + b'\n')
    print('BOUND', output, digest)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
