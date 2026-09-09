import ast
import subprocess
import sys

assert sys.version_info[:3] == (3, 14, 6)
git = 'C:/Program Files/Git/cmd/git.exe'


def blob(commit, path):
    return subprocess.run([git, '-C', 'D:/Pontius', 'cat-file', 'blob', commit + ':' + path],
                          capture_output=True, check=True).stdout.decode()


path = 'tests/test_legal_river_quotient_fixed_width_device_preflight.py'
base = blob('d8d291cc', path)
candidate = blob('9fce4bf', path)
candidate = candidate.replace('import shutil\n', '')
candidate = candidate.replace(
    'GIT = os.environ.get("PONTIUS_GIT") or shutil.which("git")\n'
    'if GIT is None or not Path(GIT).is_absolute():\n'
    '    raise RuntimeError("an absolute Git executable is required for these fixtures")\n', '')
candidate = candidate.replace('[GIT, "check-attr"', '["git", "check-attr"')
assert ast.dump(ast.parse(base)) == ast.dump(ast.parse(candidate))
for path in ('tests/test_blueprint_workload_session.py',
             'tests/test_legal_river_quotient_fixed_width_device_preflight.py'):
    assert blob('5815bfa', path) == blob('9fce4bf', path)
print('Device fixture reflow is AST-identical after reversing the authorized Git edit.')
print('Final RED and GREEN test blobs are byte-identical.')
