# Email triage case report

## CASE-001 · Escalate as suspected credential phishing

**Timeline.** The synthetic message is dated 24 November 2026 at 14:10 UTC. It claims to come from Northstar IT and asks the recipient to verify their account by the end of the day.

| Evidence | Analyst interpretation |
|---|---|
| The From domain is `northstar.example`. The Reply-To and Return-Path use `account-check.example`. | Replies and bounces go to a different domain from the stated sender. This merits investigation alongside the other evidence. |
| SPF passes for `account-check.example`, DKIM is absent, and DMARC fails for `northstar.example`. | In the simulated gateway results, SPF authenticated the envelope domain, which did not align with the visible From domain. |
| The email directs the recipient to `https[:]//account-check[.]example/verify`. | The requested account action goes to a domain outside Northstar's known domains in this scenario. |

**Disposition.** Escalate as suspected credential phishing. Set initial severity to medium pending confirmation of delivery scope and user interaction. The sample establishes a suspicious message. Whether anybody clicked, submitted credentials, or lost control of an account is unknown.

**Analyst handoff.** Preserve the message and hash. Check gateway telemetry for matching messages, delivery status, and recipients. Check available click telemetry and confirm user interaction. If credential submission is reported, escalate to identity incident response for sign-in review and account containment.

## CASE-002 · Close as expected maintenance notice

The synthetic message is dated 24 November 2026 at 14:30 UTC. The sender and reply domains align, the simulated gateway reports a DMARC pass, and the only URL points to the known status host in the scenario. The notice asks for no sign-in. Close as benign based on the combination of the expected sender, destination, and message content.
