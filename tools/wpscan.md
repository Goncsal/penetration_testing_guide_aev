# wpscan

WordPress scanner: version, themes, plugins (+versions), users, known vulns, password attacks.

```bash
wpscan --url $T                                         # basic
wpscan --url $T -e vp,vt,u,cb,dbe                       # vulnerable plugins/themes, users, config backups, db exports
wpscan --url $T -e ap --plugins-detection aggressive    # all plugins, slower, more accurate
wpscan --url $T --api-token <TOKEN>                     # vuln data (free token at wpscan.com)
wpscan --url $T -U admin,editor -P wordlists/passwords/top-1000.txt   # brute force (xmlrpc/wp-login)
wpscan --url $T --disable-tls-checks --random-user-agent
```
No token? Take versions from the output and look them up manually
([06-cve-research](../00-start/06-cve-research.md)). Docker: `docker run -it --rm wpscanteam/wpscan --url ...`
(use `--add-host` or the IP for lab names).
