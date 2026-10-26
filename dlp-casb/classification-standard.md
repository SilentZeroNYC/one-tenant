FIRST WRITE THE STANDARD (dlp-casb/classification-standard.md)

PUBLIC - anyone may see - no controls
INTERNAL - employees only - gateway use OK, no public posting
CONFIDENTIAL - limited group - no unsanctioned AI, no personal drives
RESTRICTED - named people only - block everywhere, alert on touch

DATA MOVES 3 WAYS - SO DLP SITS IN 3 PLACES
Typed into AI prompt ----> [3a] Presidio guardrail in LiteLLM
Uploaded in browser -----> [3b] Cloudflare Gateway DLP (Block)
Sitting in a file --------> [3c] LOCAL Presidio scan (find + report) - Cloud DLP API = roadmap
