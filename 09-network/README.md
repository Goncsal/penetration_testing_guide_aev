# 09 — Network services

Scan first: [port-scanning](../01-recon/port-scanning.md). Then per service:

| Port | Service | First checks |
|---|---|---|
| 161/udp | SNMP | community `public`/`private` → walk → [snmp](snmp.md) |
| 21 | FTP | `ftp host` → `anonymous`/`anonymous`; `nmap --script ftp-anon`; version (vsftpd 2.3.4 backdoor) |
| 22 | SSH | banner version; creds found elsewhere; `hydra -l user -P list ssh://host` |
| 23 | Telnet | cleartext; default creds |
| 25 | SMTP | `nc host 25` banner; `VRFY root` / `EXPN` user enumeration (`smtp-user-enum`) |
| 53 | DNS | `dig axfr @host domain` (zone transfer leaks all hostnames) |
| 80/443 | HTTP | the rest of this repo |
| 139/445 | SMB | `smbclient -L //host -N`, `enum4linux -a host`, null session shares |
| 3306 / 5432 | MySQL / Postgres | `mysql -h host -u root` (empty pw), creds from configs |
| 6379 | Redis | `redis-cli -h host` no auth → `KEYS *`, `CONFIG SET dir` webshell |
| 27017 | MongoDB | `mongosh host` no auth |
| 2049 | NFS | `showmount -e host` → mount exports |
| odd port | custom | `nc host port`, read banner/prompt; binary? → [10-pwn](../10-pwn/README.md) |

Banner → version → [06-cve-research](../00-start/06-cve-research.md).
Legacy cleartext services (Telnet, FTP, SNMPv1/v2c) are themselves findings (deck).
