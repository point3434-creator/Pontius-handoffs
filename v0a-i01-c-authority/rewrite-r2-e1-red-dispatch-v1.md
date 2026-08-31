# R2-E1 supplemental RED dispatch

Root disposition: **GO for one actual CPython 3.11.15 reproduction only**.

This dispatch is bound to handoff commit `a33574650ce2f5a2bb94213246cdca82641d13f7`, `rewrite-r2-e1-harness-v1-manifest.sha256` SHA-256 `1fb43da43a9e8afc537b2c07de02de24c7a8c56638addef2290ca97143f67c55`. The current pair is `tests-checks/rewrite-r2-e1-probe-v1.py` `7ac823d560034a140275d2447bf68bbe1f98adc8c250e61d46aedada018656a3` and `tests-checks/rewrite-r2-e1-control-v2.py` `c76a6e170062094986e7cdea90ad8e2e7737da2d38657c6f604da8eb86417ec0`. The four inputs remain bound to H `ed837198d2c83757bfb74d962af244c33f0aeae6`, manifest `a45941376da823672808050182e151f22520167d6cb24a8a9947e7b2a6c4f45e`.

Use label `e1-red01`, slot `311`, retained candidate `D:\Pontius-handoffs\v0a-i01-c-authority\rewrite-r2-checkpoint2-source-v1.py` SHA-256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`, and controller pin `c76a6e170062094986e7cdea90ad8e2e7737da2d38657c6f604da8eb86417ec0`. The candidate itself is frozen at H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`.

Run exactly:

`D:\Pontius-tools\py311\Scripts\python.exe -I -S -B -P D:\Pontius-handoffs\v0a-i01-c-authority\tests-checks\rewrite-r2-e1-control-v2.py e1-red01 311 D:\Pontius-handoffs\v0a-i01-c-authority\rewrite-r2-checkpoint2-source-v1.py 7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d --control-sha256 c76a6e170062094986e7cdea90ad8e2e7737da2d38657c6f604da8eb86417ec0`

Expected defect reproduction is finite and specific: E01 standard and E04 function-local control pass clean with exact argv; E02 module-empty and E03 module-empty-then-deleted incorrectly return without a blocker and are the only semantic failures. The harmless Models must all pass, every public call must complete, the controller must report four analyzed cases, custody and integrity must remain clean, and the child/controller exit must be semantic RED `1`. Rows in E02/E03 are allowed and are retained; their absence is not required.

Any oracle failure, analyzer exception, timeout, malformed or side-channel output, missing record, different failing case set, non-1 exit, source/watch/protected-file mismatch, dirty snapshot outside the declared overlay/payload, or incomplete receipt is not this RED. Retain it, classify it, and stop. Never execute the sensitive source as Python; it is passed only to the public static analyzer. Do not modify source bytes before the result is adjudicated.

No actual 3.14.6 execution is authorized after this anticipated RED. No fixed-twelve rerun, checkpoint3, generator work, broader suite, GPU run, or source repair is authorized by this dispatch. A source repair requires a separately recorded category-first design and root GO after the RED is independently verified.
