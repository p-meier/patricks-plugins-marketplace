---
name: report-generation
description: "This skill should be used when an agent needs to \"generate a report\", \"create research output\", \"write findings\", \"export results\", \"create executive summary\", or produce any structured research deliverable. Defines report templates for Quick, Standard, and Deep reports with quality checklists."
---

# Report Generation Skill

Generate structured research reports with executive summaries, findings, and recommendations. Three report types cover different depth levels.

## Report Types

| Type | Length | Audience | Focus |
|------|--------|----------|-------|
| **Quick Report** | 1-2 pages | Self/Team | Fast answer |
| **Standard Report** | 3-5 pages | Stakeholders | Solid overview |
| **Deep Report** | 10+ pages | Management/Decision-makers | Complete analysis |

## Quick Report Template

```markdown
# {Title}

**Research Question**: {original question}
**Date**: {date}
**Mode**: Quick Session

---

## Summary
{2-3 sentences core statement}

## Key Findings
1. {Finding 1}
2. {Finding 2}
3. {Finding 3}

## Recommendation
{Concrete action recommendation}

## Sources
- {Source 1}
- {Source 2}
```

## Standard Report Template

See `references/report-templates.md` for the full Standard Report template with sections: Executive Summary, Context, Methodology, Key Findings, Recommendations, Open Questions, Sources.

## Deep Report Template

See `references/report-templates.md` for the full Deep Report template with sections: Executive Summary, Introduction, Methodology, Meta-Principles, Detailed Findings, Synthesis, Recommendations, Risks, Appendix.

## Writing Style Guidelines

**Do:**
- Active formulations ("X shows" not "It is shown")
- Concrete numbers and facts
- Clear structure with headings
- Bullet points for readability
- Direct source references

**Don't:**
- Jargon without explanation
- Vague statements ("tends to", "somewhat")
- Overly long paragraphs (>5 sentences)
- Unsourced claims
- Redundant information

**Examples:**
- Bad: "The solution seems to offer certain advantages."
- Good: "The solution reduces processing time by 40% (Source: Case Study X)."

## Quality Checklist

Before delivering any report:

### Structure
- [ ] Executive summary sufficient for quick readers?
- [ ] Logical flow?
- [ ] All sections filled?

### Content
- [ ] Research question answered?
- [ ] All key findings sourced?
- [ ] Recommendations concrete and actionable?
- [ ] Open questions documented?

### Sources
- [ ] All claims referenced?
- [ ] Source list complete?
- [ ] A/B sources prioritized?

### Language
- [ ] No vague formulations?
- [ ] No unsourced claims?
- [ ] Management-ready language?

## Export Formats

Reports can be exported using the document processing skills:
- **xlsx skill** — For data tables, comparison matrices
- **docx skill** — For formatted Word documents
- **pdf skill** — For final PDF deliverables
- **pptx skill** — For presentation decks

## Additional Resources

### Reference Files

- **`references/report-templates.md`** — Full Standard and Deep report templates with all sections
