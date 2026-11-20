# whatweb & nikto

**whatweb** — identifies CMS, frameworks, servers, versions from headers/HTML/cookies.
```bash
whatweb -a 3 $T            # aggressive level 3
whatweb -v $T              # verbose, every plugin's evidence
```

**nikto** — noisy quick scan for known files, misconfigs, outdated servers, dangerous methods.
```bash
nikto -h $T                          # full URL ok
nikto -h host -p 8080 -Tuning 123b   # tune categories
```
Good for: finding `/phpinfo.php`, backup files, default pages, `/icons/`, old Apache, PUT enabled.
Output is a list of leads — confirm each by hand. Wappalyzer (browser extension) is the GUI
alternative.
