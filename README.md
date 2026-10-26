# ONE TENANT

**One complete corporate security program for a simulated AI-first company — built as a
hands-on lab, layer by layer, with evidence.**

One Tenant answers one question: *what does a modern corporate security program look like
when the company runs on AI?* It rebuilds the full scope of a senior corporate security
role in a single tenant — identity, an internal LLM gateway, DLP at three enforcement
points, CASB, MCP/agent governance, detection, automated response, and the written
governance that explains why every control is set the way it is.

## The system in one sentence

Identity decides who gets in, the gateway decides what the AI can do, DLP decides what
data can move, Wazuh watches all of it, Tines acts on it — and governance is why each
setting is what it is.

## The layers

| # | Layer | What it proves |
|---|---|---|
| 1 | **Foundation** — GCP IAM baseline (least-privilege service accounts, audit logging), Okta tenant (groups, MFA enrollment + session policies, OIDC SSO), Python joiner/leaver lifecycle automation | Identity is the perimeter; access is granted, reviewed, and revoked by script, not by memory |
| 2 | **LLM gateway** — LiteLLM in Docker: per-team virtual keys, budgets, full request logging; backends = local Ollama + Google AI Studio | Every AI call flows through one governed door with keys, spend caps, and logs — instead of personal API keys scattered across tools |
| 3 | **DLP at three points** — Presidio guardrail inside the gateway (pre-call PII block/mask), Cloudflare Gateway DLP + Shadow AI block at the browser, local file scans for data at rest; one written classification standard drives all three | Data classification is a written standard, enforced wherever data moves: into a prompt, through a browser, or sitting in a file |
| 4 | **CASB / SaaS** — Cloudflare CASB findings on Drive + GitHub worked end-to-end, SaaS inventory register, OAuth grant review | Shadow IT and overscoped grants are found, remediated, and *verified* — not just listed |
| 5 | **MCP governance** — an MCP file tool built raw (reads any path), then locked down: directory allowlist, scoped token, human approval, JSONL logging of every call | The model didn't change — the controls around the tool did. Agent tool access is allowlisted, gated, and logged |
| 6 | **Detection** — Wazuh collects gateway logs, MCP call logs, and Cloudflare events; three custom rules (100001–100003) turn raw lines into alerts | Every layer above reports into one place, with alerts tuned to behaviors, not vendor defaults |
| 7 | **Automated response** — Tines kill switch: alert → VirusTotal enrichment → severity gate → LiteLLM key revoked via API → GitHub issue → email | The difference between a notification and a control: a policy violation revokes the credential by itself |
| 8 | **Governance + red team** — AI tool intake questionnaire, risk-tier model, acceptable-use policy, risk register, OWASP Threat Dragon STRIDE model, controls matrix (NIST CSF 2.0 / AI RMF / CIS v8 / SOC 2), Garak + promptfoo before/after delta, live-fire exercise with NIST SP 800-61 incident reports | Governance as working documents — and controls proven by attacking them, with pass rates measured before and after |

## The honest frame

- **Lab work is presented as lab work.** Simulated users (Elena Employee, Rob Rogue),
  synthetic data only (900-series SSNs, public test card number). Nothing here is
  production corporate experience, and this repo never claims CrowdStrike Falcon,
  Netskope, or Zscaler hands-on time.
- **Built at $0 by design.** GCP's free trial needs a payment card and ~$50 hold, so no
  billing account is attached: the gateway runs in Docker on an Ubuntu workstation
  (hosting was never the control being demonstrated), secrets use the gitignored `.env`
  pattern with `chmod 600`, and the storage DLP scan runs locally with Presidio. The
  cloud-hosted deployment (GCP VM, Secret Manager, Cloud DLP API) is written up per
  layer as roadmap steps with exact commands ready to run.
- **Every claim links to evidence.** Each layer's README points at the config, log, or
  screenshot that proves it. A secrets check runs before every push.
