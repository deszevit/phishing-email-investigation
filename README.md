# Phishing email investigation

This SOC lab extracts evidence from two synthetic emails and documents why one warrants escalation and the other can be closed. It uses reserved example domains and runs locally with Python 3.10 or later. It requires no cloud account or third-party packages.

## Run the lab

From the project directory in Windows PowerShell:

```powershell
py triage.py samples/suspicious.eml
py triage.py samples/benign.eml
```

On macOS or Linux, use `python3` in place of `py`.

Compare the From, Reply-To, Return-Path, and Authentication-Results headers, then review the defanged URLs. The script prints JSON with the source file's SHA-256 hash, headers, URLs, and attachment names. See the [case report](investigation.md) for the analyst decisions.

The script makes no network requests. URL extraction is limited to visible HTTP(S) strings in decoded text and HTML MIME bodies. It does not resolve redirects, validate sender authentication, or inspect attachment contents. In a real investigation, confirm authentication results with the receiving gateway because a saved email can contain forged headers.
