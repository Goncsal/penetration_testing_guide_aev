# hashcat / John the Ripper / hashid

Offline cracking of hashes you found (dumps, JWTs).

```bash
hashid -m '<hash>'                       # guess type + hashcat mode
hashcat -m <mode> hashes.txt wordlist.txt            # dictionary
hashcat -m <mode> hashes.txt wordlist.txt -r /usr/share/hashcat/rules/best64.rule   # + mutations
hashcat -m <mode> hashes.txt -a 3 '?d?d?d?d'         # mask: 4 digits (?l lower ?u upper ?a all)
hashcat -m <mode> hashes.txt --show                  # print cracked
john --wordlist=wordlist.txt hashes.txt ; john --show hashes.txt
john --format=raw-md5 ...                             # force format
```
| Hash | hashcat `-m` |
|---|---|
| MD5 | 0 |
| SHA-1 | 100 |
| SHA-256 | 1400 |
| md5(salt.pass) / md5(pass.salt) | 20 / 10 |
| bcrypt `$2*$` | 3200 |
| md5crypt `$1$` / sha512crypt `$6$` | 500 / 1800 |
| WordPress/phpBB `$P$` | 400 |
| Django pbkdf2_sha256 | 10000 |
| NTLM | 1000 |
| JWT HS256 | 16500 (input = the whole token) |

Before cracking: is it actually **encoding**? (base64/hex) → decode instead
([credential-storage](../03-auth/credential-storage.md)). Online lookup for unsalted MD5/SHA1:
crackstation.net.
