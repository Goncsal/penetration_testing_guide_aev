# searchsploit (Exploit-DB offline)

```bash
sudo apt install exploitdb ; searchsploit -u        # install / update
searchsploit wordpress 6.9                          # search (terms are ANDed)
searchsploit -t vsftpd                              # title only
searchsploit --cve 2021-41773                       # by CVE
searchsploit -x 49757                               # read
searchsploit -m 49757                               # copy to cwd
searchsploit --nmap scan.xml                        # match nmap -sV -oX output
```
Exploit-DB is not complete: also search GitHub (`"CVE-XXXX-YYYY" poc`), vendor advisories, NVD,
CISA KEV — see [06-cve-research](../00-start/06-cve-research.md). Always read an exploit before
running it and fix hard-coded paths/hosts.
