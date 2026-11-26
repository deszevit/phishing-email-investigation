"""Extract evidence from a saved email without making network requests."""

import argparse
import hashlib
import json
import re
from email import policy
from email.parser import BytesParser
from pathlib import Path


def extract_evidence(raw):
    message = BytesParser(policy=policy.default).parsebytes(raw)
    urls = set()
    for part in message.walk():
        if part.get_content_type() not in {"text/plain", "text/html"}:
            continue
        if part.get_content_disposition() == "attachment" or part.get_filename():
            continue
        for url in re.findall(r"""https?://[^\s<>"']+""", part.get_content(),
                              flags=re.IGNORECASE):
            urls.add(url.rstrip(".,;)").replace("://", "[:]//").replace(".", "[.]"))

    headers = (
        "Subject", "From", "Reply-To", "Return-Path", "Date", "Message-ID",
        "Authentication-Results", "Received",
    )
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "headers": {
            name: [str(value) for value in message.get_all(name, [])]
            for name in headers
        },
        "defanged_urls": sorted(urls),
        "attachment_names": [
            part.get_filename() for part in message.walk() if part.get_filename()
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email", type=Path, help="Path to a saved .eml file")
    args = parser.parse_args()
    try:
        evidence = extract_evidence(args.email.read_bytes())
    except (OSError, ValueError) as error:
        parser.exit(1, f"Unable to process email: {error}\n")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
