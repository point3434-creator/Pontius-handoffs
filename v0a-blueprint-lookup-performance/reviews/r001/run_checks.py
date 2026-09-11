import io,json,os,pathlib,sys,tempfile,unittest
S=pathlib.Path(__file__).resolve().parent
C=S/'candidate'
os.chdir(C)
os.environ['TMP']=os.environ['TEMP']=str(S/'temp')
(S/'temp').mkdir(exist_ok=True)
tempfile.tempdir=str(S/'temp')
sys.path[:0]=[str(C/'src'),str(C/'tests'),str(C)]
modules=json.loads((S/'suite-modules.json').read_text())
excluded=['test_blueprint_workload_session','test_eval_protocol']
modules=[m for m in modules if m not in excluded]+['test_eval_export','test_eval_completion_tool']
loader=unittest.TestLoader()
def leaves(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from leaves(item)
        else: yield item
omit=('test_real_host_check_hit_default_and_changed_stack_are_distinct',
      'test_supervised_three_phase_subset_and_bound_input_failures')
suite=unittest.TestSuite(t for m in modules for t in leaves(loader.loadTestsFromName(m))
                        if t.id().split('.')[-1] not in omit)
with (S/'tests.log').open('w') as log:
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
summary=dict(python=sys.version,tests=result.testsRun,failures=len(result.failures),
             errors=len(result.errors),skipped=len(result.skipped),
             excluded_modules=excluded,excluded_methods=omit,
             reason='Keep execution pure; excluded suites use Git commits or execution-host phases.')
(S/'test-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
if not result.wasSuccessful():
    print('\n'.join(str(t)+'\n'+err for t,err in result.failures+result.errors))
sys.exit(not result.wasSuccessful())
