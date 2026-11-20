# git-dumper

Downloads an exposed `.git/` directory (even without directory listing) and rebuilds the repo.

```bash
pip install git-dumper
git-dumper http://leak4.chal.deti:8013/.git/ out
cd out && git log --all --oneline && git log -p --all | grep -n 'flag{'
```
Alternatives: GitTools (`gitdumper.sh` + `extractor.sh` to recover every commit as folders),
`wget -r -np $T/.git/` (only with listing). Manual: [exposed-git](../02-info-leak/exposed-git.md).
