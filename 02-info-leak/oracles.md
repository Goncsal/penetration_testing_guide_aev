# Oracles (reconstruct a secret one character at a time)

**Signs**: an endpoint answers a guess with only yes/no — status 200 vs 403/404, "valid"/"invalid",
true/false, a count, a visible row, or a slower response. Hint "it only says yes", "one letter,
then another".

## Find the oracle
- Endpoint names: `/oracle`, `/check`, `/verify`, `/validate`, `/exists`, `/startswith`, `/compare`
- Params: `prefix=`, `guess=`, `q=`, `code=`, `token=`
- Test: `?prefix=f` → yes, `?prefix=x` → no. Then `?prefix=fl`, `?prefix=fla`, …

## Exploit (generic script)
```bash
python scripts/leak/prefix_oracle.py "$T/oracle?prefix={}" --start 'flag{' \
       --true-status 200
python scripts/leak/prefix_oracle.py "$T/check?guess={}" --true-text 'correct'
python scripts/leak/prefix_oracle.py "$T/check" --post 'code={}' --true-text 'Yes' --charset hex
```
Options: `--true-status`, `--true-text`, `--false-text`, `--charset` (`flag` default =
`a-z0-9{}_`, `hex`, `printable`), `--start`, `--stop '}'`, `-c COOKIE`.

## Variants
| Oracle type | Use |
|---|---|
| status/text | prefix_oracle.py |
| response **length** | `--true-len N` / compare with `--false-len` |
| timing (`strcmp` char-by-char, `sleep`) | measure per char; median of several requests |
| SQL boolean/time | [06-sqli/boolean-blind](../06-sqli/boolean-blind.md), [time-blind](../06-sqli/time-blind.md) |

Seen in: `leak7` (`/oracle?prefix=` → 200 when the flag starts with the prefix; charset `[a-z0-9{}_]`).
