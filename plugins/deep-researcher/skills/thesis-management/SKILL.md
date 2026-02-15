---
name: thesis-management
description: "This skill should be used when an agent needs to \"track theses\", \"manage hypotheses\", \"validate a thesis\", \"update THESES.md\", \"formulate a hypothesis\", or work with the research thesis lifecycle. Defines the file format, status workflow, and quality criteria for research hypotheses."
---

# Thesis Management Skill

Track, validate, and manage research theses throughout the research process using a structured lifecycle in THESES.md.

## Thesis Lifecycle

```
Open → Under Review → Validated
                  ↘ Refuted
```

| Status | Symbol | Meaning |
|--------|--------|---------|
| Open | `[ ]` | Newly formulated, not yet reviewed |
| Under Review | `[~]` | Evidence being collected |
| Validated | `[x]` | Confirmed by evidence |
| Refuted | `[!]` | Disproven by evidence |

## THESES.md File Format

```markdown
# Theses - {Project Name}

Last updated: {date}
Total: {n} | Open: {x} | Under Review: {y} | Validated: {z} | Refuted: {w}

---

## Open

- [ ] **T1**: {Thesis as a clear statement}
  - **Source**: {Initial source suggesting this thesis}
  - **Note**: {What still needs to be done}
  - **Created**: {date}

## Under Review

- [~] **T3**: {Thesis}
  - **Supports**:
    - {Source 1}: {Key statement}
    - {Source 2}: {Key statement}
  - **Contradicts**:
    - {Source 3}: {Counter-argument}
  - **Status**: {What needs to be clarified next}

## Validated

- [x] **T4**: {Thesis}
  - **Evidence**:
    - {Source 1}: {Proof}
    - {Source 2}: {Proof}
    - {Source 3}: {Proof}
  - **Confidence**: {High|Medium}

## Refuted

- [!] **T5**: {Original thesis}
  - **Refutation**: {Why wrong}
  - **Source**: {Disproving source}
  - **Instead**: → T{n} (reference to revised thesis)
```

## Thesis Quality Criteria

A good thesis is:

1. **Specific** — "75% of Fortune 500 will have GenAI in production by 2025" not "AI will become more important"
2. **Testable** — "RAG systems have higher accuracy than fine-tuning for domain knowledge" not "The technology is interesting"
3. **Relevant** — Answers part of the research question, has practical implications
4. **Sourced** — At least one source reference at creation, at least 3 sources for validation

## Confidence Levels

| Level | Criteria |
|-------|----------|
| **High** | 3+ high-quality sources, no contradictions, current data |
| **Medium** | 2+ sources, minor limitations, or older data |
| **Low** | 1 source, or significant limitations |

## Workflow: Create Thesis

1. Note observation from source
2. Formulate generalizable statement
3. Check: Is it specific? Testable?
4. Reference initial source
5. Set status "Open"
6. Assign sequential ID

## Workflow: Review Thesis

1. Set thesis to "Under Review"
2. Search specifically for supporting evidence
3. Search specifically for counter-examples
4. Document pro/contra
5. If >3 supporting sources and 0 contradictions → Validate
6. If strong contradiction → Checkpoint with user

## Workflow: Resolve Contradiction

1. Document both positions
2. Compare source quality
3. Check context (timing, scope, methodology)
4. If unresolvable → Checkpoint with user
5. Document decision
6. Adjust or refute thesis

## Integration with Other Components

### → Source-Scout
When new source found, check which theses it supports/contradicts.

### → Synthesizer
For meta-principle extraction, use validated theses as foundation.

### → Report Generation
- Validated theses → Findings
- Refuted theses → "Initially assumed but disproven"
- Open theses → "Further research needed"
