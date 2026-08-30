import hashlib,json,pathlib,sys
assert sys.version_info[:3]==(3,11,15)
ledger=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\progress.md')
checks=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r008\checks')
expected='4ec25cba0a4a59dcb319e058809e93d61e22821cad6b4053915f1b59b862818a'
line='- 2026-08-30 | r008 | Codex A | NOT CLEAN | design STRAINED | candidate 00db06624ab25f10cd181badccf92c87a78f17ee | manifest 1e5814b2c04a0065586d8fa73f89edc1ffb0eae4830bea8c893630172d5798f2 | report r008/reviews/review-01-codex-a.md SHA256 c1fcee6c2d94cbdd8ba10ca398461b6c26c055324df3c2bfc971fc78879bff4a | Important R008-A-01/A-02: comprehension and class-qualifier receiver provenance; both slots focused green but independent binding refusals fail.\n'
with ledger.open('r+b') as file:
 before=file.read();assert len(before)==5948 and hashlib.sha256(before).hexdigest()==expected
 assert before.endswith(b'\n')
 file.seek(0,2);file.write(line.encode());file.flush()
after=ledger.read_bytes();assert after==before+line.encode()
receipt={'exclusive_slot_granted_by':'parent coordinator','before_bytes':len(before),'before_sha256':expected,'appended_line':line,'after_bytes':len(after),'after_sha256':hashlib.sha256(after).hexdigest(),'prefix_preserved':True}
with (checks/'codex-a-18-ledger-append.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2))