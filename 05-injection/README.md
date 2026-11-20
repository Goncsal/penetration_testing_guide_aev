# 05 — Injection (CWE-77 family) & friends

One mistake everywhere: **data handed to an interpreter that treats part of it as code**.
Identify the interpreter → speak its syntax.

| Interpreter | Trigger | Note |
|---|---|---|
| OS shell (`sh -c`, `system`, `popen`, `exec.Command("sh","-c")`) | host/file/dir/name fields | [cmdi](cmdi.md) |
| …with a denylist | `;` stripped/blocked | [cmdi-filter-bypass](cmdi-filter-bypass.md) |
| …behind a WAF | 403 "blocked" | [cmdi-waf-evasion](cmdi-waf-evasion.md) |
| …but output not shown | no echo | [cmdi-blind-oob](cmdi-blind-oob.md) |
| …stored now, executed later | config/save + run/ship | [cmdi-second-order](cmdi-second-order.md) |
| …program **name** resolved via PATH | upload plugin/tool | [cmdi-path-hijack](cmdi-path-hijack.md) |
| Target program's own options (CWE-88) | tar/find/curl/git args | [argument-injection](argument-injection.md) |
| Template engine (Jinja2, EJS, Twig…) (CWE-94/1336) | `{{7*7}}` → 49 | [ssti](ssti.md) |
| Language `eval`/`include`/regex `/e` (CWE-94/624) | PHP/Python code paths | [code-injection](code-injection.md) |
| XML parser with DTDs (CWE-611) | XML import | [xxe](xxe.md) |
| URL fetcher (CWE-918) | "preview URL" | [ssrf](ssrf.md) |
| Deserializer (CWE-502) | pickle/yaml/Java/PHP blobs | [deserialization](deserialization.md) |
| Filesystem path (CWE-22/98) | `?file=`, `?page=` | [lfi-path-traversal](lfi-path-traversal.md) |
| Web server executing uploads | upload forms | [file-upload](file-upload.md) |
| bash env parsing (CVE-2014-6271) | CGI scripts | [shellshock](shellshock.md) |
| LLM prompt (CWE-1427) | chatbot/agent | [prompt-injection](prompt-injection.md) |
| SQL | → [06-sqli](../06-sqli/README.md) |
| HTML/JS in browser | → [07-xss](../07-xss-client-side/README.md) |

## Universal probe
Send each into every input and watch for errors, delays, `49`, or changed output:
```
;id   |id   `id`   $(id)   %0aid   '   "   {{7*7}}   ${7*7}   <%= 7*7 %>   #{7*7}   ../../../../etc/passwd   <x>
```
`python scripts/injection/probe.py "$T/ping" --data 'host=FUZZ'` automates this and reports which
class reacted.

Course map: inj1 `;` · inj2 newline · inj3 Jinja2 SSTI · inj4 XXE · inj5 `;` in tar arg · inj6 EJS
SSTI · inj7 `$()` into a log · inj8 glob `*` · inj9 SSRF `file://` · inj10 PATH hijack · inj11
second-order · inj12 pickle · inj13 exec API / `$()` + octal `printf` · inj14 HPP / double-encoding.
