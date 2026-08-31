# Rewrite R1 Gate A harness — authoring handoff v1

Frozen, unexecuted. Root independently reviews these bytes before any dispatch.
Exactly Gate A6/8 from population 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce; no Gate B.

- Probe: rewrite-r1-probe-v1.py c0672ac61fa19b5dd3d46fc6c0dbbdaae4565c610e7e658619c738559fb27395
- Control: rewrite-r1-control-v1.py 9310da3cecabaae0127fb6562a15b388355f722c35dcd5abbd2b039fd0f4d48c
- Plan: rewrite-r1-plan-v1.md 8cec0f3af002f04b20c82dee62d29f0601a87047249ab2dfcde5a164ca73826d
- Observer map: rewrite-r1-observer-map-v1.json af8df00ceb6b02bb5730eee56754ce78badcab6102ce861d726eed704522bfbd
- Static proof: rewrite-r1-static-v1.json (hash printed on issuance)
- Exact controller/probe predecessor diffs retained separately.

Original public functions and Model runners compare AST-equal (storage public
definition name alone is changed). Source strings remain original pack bytes;
only harmless Models compile/execute in the future child. Both complete packs,
population, observer map, plan, control, probe and retained candidate are pinned.
The control's filesystem/environment/Git/hash primitives are unchanged.

Budget observation wraps only original init/consume; source consume segment
d910a8af42711e5130b93af9e55b8917dbd8b48433e29e1ab3cd51df63b7af5c is verified before import on both slots. All epochs,
throwing requests and nearest caller/phase totals are retained and reconciled.
No original calls or charges are suppressed, no budget/cache/AST/frame retained.
Observer overhead is disclosed; production-operation accounting is a separate
source-review obligation. Gate A applies unchanged production caps only.

Root-owned future CLI (not executed here):
D:/Pontius-tools/py311/Scripts/python.exe -I -S -B -P <control> LABEL 311 <retained-source.py> SOURCE_SHA --control-sha256 9310da3cecabaae0127fb6562a15b388355f722c35dcd5abbd2b039fd0f4d48c --worktree-sha256 APPROVED_CORE_WORKTREE_SHA
Dev additionally requires --floor-receipt <path> --floor-sha256 <SHA> and an
intact matching semantic/accounting GREEN floor result. RED cannot unlock dev.
Each invocation creates a new snapshot/temp and exclusive outputs. Old-W v20
watch remains; new core-W watch is explicit and pinned per invocation.
The unmodified r010 generator is legal RED input and expects no tracked diff.

No source/W/candidate edits, payload, Git mutation, installation, fixture generation,
new expected outcome, old diagnostic, or orchestration owner was invoked.
Static checks do not establish that this unexecuted harness works at runtime.
