import json,os,pathlib,subprocess,sys
S=pathlib.Path(__file__).resolve().parent
P=pathlib.Path('D:/Pontius-handoffs/v0a-blueprint-lookup-performance/r001')
records=[]
for script in ('benchmark.py','retained-parity.py'):
    for variant in ('base','candidate'):
        out=S/(script.removesuffix('.py')+'-'+variant+'.json')
        args=[str(out)] if script=='benchmark.py' else [str(P/'inputs/blueprint.json'),str(P/'inputs/teacher.json'),str(out)]
        command=[sys.executable,'-B','-c',
                 'import sys,runpy;sys.path.insert(0,sys.argv.pop(1));p=sys.argv.pop(1);sys.argv[0]=p;runpy.run_path(p,run_name="__main__")',
                 str(S/variant/'src'),str(P/'checks'/script),*args]
        result=subprocess.run(command,cwd=S,capture_output=True,text=True,timeout=120)
        (S/(script+'-'+variant+'.log')).write_text(result.stdout+result.stderr)
        records.append(dict(script=script,variant=variant,exit_code=result.returncode,command=command))
        print(script,variant,result.returncode,flush=True)
        if result.returncode: print(result.stderr); break
b=json.loads((S/'retained-parity-base.json').read_text()); c=json.loads((S/'retained-parity-candidate.json').read_text())
comparison={k:b[k]==c[k] for k in b if k!='diagnostic_membership_seconds'}
assert all(comparison.values()),comparison
(S/'diagnostics-summary.json').write_text(json.dumps(dict(commands=records,parity_comparison=comparison),indent=2)+'\n')
print('Full parity equality:',comparison,flush=True)
