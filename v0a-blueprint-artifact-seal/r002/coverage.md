# Mechanical correction coverage

Invariant: governance metadata is LF-only and generated STATUS retains exactly
the unchanged renderer's text. The r001 frozen STATUS had 88 CRLF endings because
the CLI wrote text with platform translation. All 14 paths were enumerated by
raw Git diff; only STATUS had this metadata defect. Regeneration in a fresh floor
snapshot through unchanged render_status().encode('utf-8') removes exactly those
88 CR bytes. No textual content, ADR, source, fixture, registration, profile,
boundary, analyzer or CI byte changes relative to r001.

Falsifier: any r001-to-r002 path other than STATUS, or any byte difference other
than CRLF-to-LF, invalidates this correction-only claim. Raw diff, explicit byte
comparison and all-file manifest audit verify it. Post-CLEAN generator --check
and the unchanged 12-test status suite remain mandatory on both slots. This
claim does not treat universal-newline text equality as proof of raw hygiene.
