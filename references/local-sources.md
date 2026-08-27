# Local IELTS source routing

Use local sources only when present in the active workspace. Run the compact indexer before opening source files:

```bash
python scripts/retrieve_topic_sources.py --workspace /absolute/workspace --keywords <2-6 bilingual topic keywords>
```

The command returns primary vocabulary PDF page numbers, available writing/speaking banks, wordlist paths, and capped matching JSON records. Inspect only the returned pages or records. Do not load whole books into model context.

## Primary structural reference

`English for Everyone English Vocabulary Builder (Dorling Kindersley, Inc.) (Z-Library).pdf`

Use its topic organisation, visual vocabulary, ordinary expressions, short definitions, and progression into practice. Do not copy its page design or reproduce substantial text.

## Writing and idea banks

- `雅思写作/雅思写作大作文语料库进阶.pdf`
- `雅思写作/雅思大作文15个常见话题论点参考.pdf`
- `雅思写作/Ideas_for_IELTS_topics_（simon）.pdf`

Open only topic-relevant pages when Card 4 or Card 5 needs wider argument functions. Pass every candidate through `language-quality.md`.

## Speaking banks

- `雅思口语/雅思口语50道part 2高分素材.pdf`
- `雅思口语/雅思口语20道part 3高分素材.pdf`
- `雅思口语/《雅思口语必备900句》.pdf`

Use short natural chunks and personal or social angles, not memorised answers.

## Structured word lists

- `ielts_core.json`
- `cet4.json`
- `vocabulary.json`

Use matching records as recall aids or level filters, not proof that an item belongs in the scene.

## Token and copyright discipline

- Prefer a page number or short matching record over full extraction.
- Cap retrieval output; request another keyword pass only when the first pass is genuinely insufficient.
- Do not embed, duplicate, or redistribute source PDFs.
