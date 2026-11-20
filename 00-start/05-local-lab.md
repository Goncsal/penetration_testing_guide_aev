# Running challenges locally

The course repo (`aev-ctf`) has one folder per challenge with `Dockerfile` + `docker-compose.yml`.
Local override files (`aev-local-compose/<name>.yml`) bind each one to `127.0.0.1:<port>`.

```bash
cd aev-ctf/inj/inj1
docker compose up -d --build                         # lab-style port
# or with the local override (binds 127.0.0.1 only):
docker compose -f docker-compose.yml -f ../../../aev-local-compose/inj1.yml up -d --build
docker compose logs -f                                # watch the app
docker compose down -v                                # clean up
```

Inside the container (to understand what you're attacking — **not** possible on the real lab):
```bash
docker compose exec <service> sh
```

## Lab vs local addresses

| Category | Lab host | Local port range |
|---|---|---|
| infoleak | `leakN.chal.deti` | 8010–8019 |
| web intro (notes1, xss1-3) | `notes1/xssN.chal.deti` | 8020–8023 |
| network (snmp1) | `snmp1.chal.deti` | 8024/udp |
| sqli | `sqliN.chal.deti` | 8030–8037 |
| inj | `injN.chal.deti` | 8040–8053 |
| auth | `authN.chal.deti` | 8060–8073 |
| bwapp / dvwa / mutillidae / wordpress | `<name>.chal.deti` | 8081 / 8082 / 8083 / 8084 |
| juiceshop | `juiceshop.chal.deti` | 3000 |
| pwn1 | `pwn1.chal.deti` | 9001 (nc) |

Full table: [challenges/README.md](../challenges/README.md).

## Lab network notes

- Out-of-band callbacks from lab containers: the lab egress filter only lets **80/443** out — run
  your listener on 443 (needs root) or 80. See [tools/oob-listeners.md](../tools/oob-listeners.md).
- `*.chal.deti` is a wildcard: `marketing.auth6.chal.deti` resolves to the same box (vhost tricks).
- Locally, a vhost needs `-H 'Host: marketing.auth6.chal.deti'` or an `/etc/hosts` entry.
