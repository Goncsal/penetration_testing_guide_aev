# Burp Suite (Community) / OWASP ZAP

Intercepting proxy: see and edit every request your browser makes.

Setup: Burp → Proxy → "Open browser" (pre-configured Chromium). Or set browser proxy
`127.0.0.1:8080` and install Burp's CA (`http://burp`).

| Tab | Use in these challenges |
|---|---|
| **Proxy → HTTP history** | see hidden requests (XHR/API calls, cookies set, redirects) |
| **Repeater** (Ctrl+R) | edit & resend one request: change cookies (`role=manager`), headers (`Referer`), params, bodies (XML/JSON) |
| **Intruder** | fuzz one position (slow in Community — prefer [ffuf](ffuf.md)) |
| **Sequencer** | collect many session tokens → randomness analysis ([predictable-tokens](../03-auth/predictable-tokens.md)) |
| **Decoder** | base64/URL/hex encode/decode |
| **Comparer** | diff two responses (user enumeration, boolean SQLi) |
| Extensions | JWT Editor (JWT attacks), Param Miner (hidden params), Autorize (IDOR) |

Tips: "Copy as curl command" from history → reproduce in a script. Send ffuf/sqlmap through Burp
(`-x http://127.0.0.1:8080` / `--proxy`) to inspect what they send.

ZAP equivalent: Manual Explore, Request Editor, Fuzzer; free and scriptable.
