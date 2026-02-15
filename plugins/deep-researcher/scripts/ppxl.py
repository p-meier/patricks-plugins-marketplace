#!/usr/bin/env python3
"""Perplexity API CLI for Deep Researcher plugin.

Uses the official perplexityai SDK. Cost tiers per request:

  search         ~$0.005    Raw search results, source discovery (use freely)
  ask            ~$0.01     AI answer with sonar (cheap, good for quick questions)
  ask --pro      ~$0.05     AI answer with sonar-pro (better quality, citations)
  reason         ~$0.10     Complex analysis with sonar-reasoning-pro
  deep-research  ~$0.50-2+  Multi-step deep research (EXPENSIVE, checkpoint only)

Usage:
  ppxl.py search "query" [--domains d1,d2] [--recency day|week|month] ...
  ppxl.py ask "query" [--pro] [--domains d1,d2] [--recency day|week|month]
  ppxl.py reason "query"
  ppxl.py deep-research "query" --confirm
"""

import argparse
import json
import sys
import os


def get_client():
    try:
        from perplexity import Perplexity
    except ImportError:
        print("Error: perplexityai package not installed.", file=sys.stderr)
        print("Run: bash ${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("PERPLEXITY_API_KEY"):
        print("Error: PERPLEXITY_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    return Perplexity()


def parse_domains(domains_str):
    """Parse comma-separated domains into list."""
    if not domains_str:
        return None
    return [d.strip() for d in domains_str.split(",") if d.strip()]


def cmd_search(args):
    """Search API - raw results, cheapest tier (~$0.005/request)."""
    client = get_client()

    kwargs = {"query": args.query}

    if args.max_results:
        kwargs["max_results"] = args.max_results
    if args.domains:
        kwargs["search_domain_filter"] = parse_domains(args.domains)
    if args.exclude_domains:
        kwargs["search_domain_filter"] = [f"-{d}" for d in parse_domains(args.exclude_domains)]
    if args.recency:
        kwargs["search_recency_filter"] = args.recency
    if args.language:
        kwargs["search_language_filter"] = parse_domains(args.language)
    if args.country:
        kwargs["country"] = args.country

    response = client.search.create(**kwargs)

    if args.output == "json":
        results = []
        for r in response.results:
            results.append({
                "title": getattr(r, "title", ""),
                "url": getattr(r, "url", ""),
                "snippet": getattr(r, "snippet", ""),
                "date": getattr(r, "date", None),
            })
        print(json.dumps({"query": args.query, "result_count": len(results), "results": results}, indent=2))
    else:
        print(f"# Search Results: {args.query}\n")
        for i, r in enumerate(response.results, 1):
            title = getattr(r, "title", "Untitled")
            url = getattr(r, "url", "")
            date = getattr(r, "date", None)
            snippet = getattr(r, "snippet", "")
            print(f"## {i}. {title}")
            print(f"**URL:** {url}")
            if date:
                print(f"**Date:** {date}")
            if snippet:
                print(f"\n{snippet}")
            print("\n---\n")


def cmd_ask(args):
    """Sonar API - AI-grounded answer with web search."""
    client = get_client()

    model = "sonar-pro" if args.pro else "sonar"

    web_search_options = {}
    if args.domains:
        web_search_options["search_domain_filter"] = parse_domains(args.domains)
    if args.exclude_domains:
        web_search_options["search_domain_filter"] = [f"-{d}" for d in parse_domains(args.exclude_domains)]
    if args.recency:
        web_search_options["search_recency_filter"] = args.recency

    kwargs = {
        "messages": [{"role": "user", "content": args.query}],
        "model": model,
    }
    if web_search_options:
        kwargs["web_search_options"] = web_search_options

    completion = client.chat.completions.create(**kwargs)

    content = completion.choices[0].message.content
    citations = getattr(completion, "citations", []) or []

    if args.output == "json":
        print(json.dumps({"model": model, "content": content, "citations": citations}, indent=2))
    else:
        print(f"# Answer ({model})\n")
        print(content)
        if citations:
            print("\n## Citations\n")
            for i, c in enumerate(citations, 1):
                print(f"{i}. {c}")


def cmd_reason(args):
    """Sonar Reasoning Pro - complex analysis (~$0.10/request)."""
    client = get_client()

    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": args.query}],
        model="sonar-reasoning-pro",
    )

    content = completion.choices[0].message.content
    citations = getattr(completion, "citations", []) or []

    if args.output == "json":
        print(json.dumps({"model": "sonar-reasoning-pro", "content": content, "citations": citations}, indent=2))
    else:
        print("# Reasoning Analysis\n")
        print(content)
        if citations:
            print("\n## Citations\n")
            for i, c in enumerate(citations, 1):
                print(f"{i}. {c}")


def cmd_deep_research(args):
    """Sonar Deep Research - EXPENSIVE (~$0.50-2.00+ per call)."""
    if not args.confirm:
        cost_msg = (
            "WARNING: deep-research uses sonar-deep-research (~$0.50-2.00+ per call).\n"
            "It triggers multiple internal searches and produces extensive output.\n"
            "Only use at checkpoints, never in automated loops.\n\n"
            "Add --confirm to proceed."
        )
        print(cost_msg, file=sys.stderr)
        sys.exit(1)

    client = get_client()

    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": args.query}],
        model="sonar-deep-research",
    )

    content = completion.choices[0].message.content
    citations = getattr(completion, "citations", []) or []

    if args.output == "json":
        print(json.dumps({"model": "sonar-deep-research", "content": content, "citations": citations}, indent=2))
    else:
        print("# Deep Research Results\n")
        print(content)
        if citations:
            print("\n## Citations\n")
            for i, c in enumerate(citations, 1):
                print(f"{i}. {c}")


def main():
    parser = argparse.ArgumentParser(
        description="Perplexity API CLI for Deep Researcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Cost tiers:
  search         ~$0.005/req    Use freely for source discovery
  ask            ~$0.01/req     Quick factual questions
  ask --pro      ~$0.05/req     Detailed answers with citations
  reason         ~$0.10/req     Complex analysis
  deep-research  ~$0.50-2+/req  ONLY at checkpoints, requires --confirm""",
    )
    parser.add_argument("--output", "-o", choices=["json", "markdown"], default="markdown",
                        help="Output format (default: markdown)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- search ---
    p_search = subparsers.add_parser("search", help="Raw search results (~$0.005/req)")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--max-results", type=int, default=10, help="Max results 1-20 (default: 10)")
    p_search.add_argument("--domains", help="Comma-separated domain allowlist (e.g. nature.com,arxiv.org)")
    p_search.add_argument("--exclude-domains", help="Comma-separated domain denylist (e.g. reddit.com,pinterest.com)")
    p_search.add_argument("--recency", choices=["day", "week", "month"], help="Recency filter")
    p_search.add_argument("--language", help="Comma-separated ISO 639-1 codes (e.g. en,de)")
    p_search.add_argument("--country", help="ISO 3166-1 alpha-2 code (e.g. US, DE, GB)")

    # --- ask ---
    p_ask = subparsers.add_parser("ask", help="AI-grounded answer (sonar/sonar-pro)")
    p_ask.add_argument("query", help="Question to answer")
    p_ask.add_argument("--pro", action="store_true", help="Use sonar-pro model (higher quality, more expensive)")
    p_ask.add_argument("--domains", help="Comma-separated domain allowlist")
    p_ask.add_argument("--exclude-domains", help="Comma-separated domain denylist")
    p_ask.add_argument("--recency", choices=["day", "week", "month"], help="Recency filter")

    # --- reason ---
    p_reason = subparsers.add_parser("reason", help="Complex reasoning with sonar-reasoning-pro (~$0.10/req)")
    p_reason.add_argument("query", help="Question requiring deep analysis")

    # --- deep-research ---
    p_deep = subparsers.add_parser("deep-research", help="EXPENSIVE deep research (~$0.50-2+/req)")
    p_deep.add_argument("query", help="Research question")
    p_deep.add_argument("--confirm", action="store_true", help="Confirm expensive operation (required)")

    args = parser.parse_args()

    try:
        if args.command == "search":
            cmd_search(args)
        elif args.command == "ask":
            cmd_ask(args)
        elif args.command == "reason":
            cmd_reason(args)
        elif args.command == "deep-research":
            cmd_deep_research(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
