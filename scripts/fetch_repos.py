#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "index.template.html"
PLACEHOLDER = "/*__REPO_DATA__STARTJSON*/{}/*__REPO_DATA__ENDJSON*/"
API_URL = (
    "https://api.github.com/search/repositories"
    "?q=stars:>1&sort=stars&order=desc&per_page=100&page=1"
)


def fetch_top_repos(token: str) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(API_URL, headers=headers, timeout=30)

    remaining = response.headers.get("X-RateLimit-Remaining", "unknown")
    if remaining == "0":
        reset = response.headers.get("X-RateLimit-Reset", "unknown")
        print(f"Rate limit exhausted. Resets at: {reset}", file=sys.stderr)
        sys.exit(1)

    if not response.ok:
        print(f"API error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    data = response.json()
    items = data.get("items", [])
    result = []
    for idx, item in enumerate(items):
        result.append({
            "rank": idx + 1,
            "full_name": item["full_name"],
            "html_url": item["html_url"],
            "description": item.get("description") or "",
            "stargazers_count": item["stargazers_count"],
            "forks_count": item["forks_count"],
            "language": item.get("language") or "",
            "pushed_at": item.get("pushed_at") or "",
        })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="index.html")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is not set")

    print("Fetching top 100 repos from GitHub API...")
    items = fetch_top_repos(token)
    print(f"Fetched {len(items)} repos. Top: {items[0]['full_name']} ({items[0]['stargazers_count']:,} stars)")

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "items": items,
    }

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"Placeholder '{PLACEHOLDER}' not found in template", file=sys.stderr)
        sys.exit(1)

    output = template.replace(PLACEHOLDER, json.dumps(payload, ensure_ascii=False))
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"Written to {args.output}")


if __name__ == "__main__":
    main()
