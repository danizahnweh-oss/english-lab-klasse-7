# English Lab · Klasse 7

A public, mobile-friendly self-study site for a German Gymnasium class 7. It follows the English Lab class 10 design, but uses the supplied class 7 exams and its own independent practice bank. No fixed study dates or assumed exam date.

- 196 newly authored grammar exercises (95 text inputs, 73 choices, 14 sentence puzzles and 14 error hunts), 14 German reference chapters, three levels per topic.
- Independent diagnostic, mixed rounds, feedback and mistake practice. Original questions are not used in advance practice.
- Complete editable original tests 2021–2025: listening (20 BE), Use of English (20 BE), text production (20 BE). Optional 50-minute timer.
- Original audio, picture choices and writing materials included. Original correction exercises and word boxes retained, with mobile-adapted layout and numbered answer fields.
- Grammar and closed-choice listening checked against the supplied official keys. Free listening and writing require explicit self-assessment. No automatic grading of free text or secure teacher submission.
- Local autosave, resume and answer-sheet download. No account, tracking or external fonts. Learner data stays in this browser; a shared device exposes locally stored work to its other users. Hosting providers process normal website requests.

## Run
Serve `dist/` with a static HTTP server. No framework or build step required. Hash routing supports static hosts. Optional WebMCP `start_grammar_practice` uses the same visible flow when supported; normal browser use does not depend on it.

## Content maintenance
`content/practice.txt` and `content/build-practice.py` generate `dist/data.js`.
`content/build-exams.py` uses transcribed source text and manually verified official keys to generate `content/exams.json` and `dist/exams-data.js`. Run this before `build-practice.py` when exam metadata changes. Teacher-supplied PDFs remain unchanged in `dist/material/`. Audio files are complete AAC copies at 96 kbps; the original MP3 files remain at the teacher-supplied source location. Duration is verified against the original after conversion. Historical claims and dates belong to those original tasks.
`content/build-assets.py` renders and crops the supplied original PDF figures using pypdfium2 and Pillow; it creates no new illustrations.

## Validation
`tests/verify.cjs` checks practice keys, levels, all five complete exam totals, solution visibility, answer locking, timers, persistence, local assets and form labels using jsdom. Run with Node and jsdom available. These are emulated DOM checks, not native browser or WebMCP validation; no browser visual QA was requested.

## Publication
GitHub Actions publishes `dist/` through GitHub Pages. `.openai/hosting.json` records this class 7 Sites project. It is independent of the existing class 10 platform. Credentials are not stored in source.
