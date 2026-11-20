#!/usr/bin/env bash
# Download wordlists that are too big for git (run from the repo root or anywhere).
#   bash wordlists/fetch_big.sh            # rockyou + big dir lists
# Output goes to wordlists/big/ (git-ignored).
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)/big"
mkdir -p "$D"
S=https://raw.githubusercontent.com/danielmiessler/SecLists/master

fetch() { echo "[*] $2"; curl -fL --progress-bar -o "$D/$1" "$2"; }

# rockyou (~133 MB unpacked)
if [ ! -f "$D/rockyou.txt" ]; then
  fetch rockyou.txt.tar.gz "$S/Passwords/Leaked-Databases/rockyou.txt.tar.gz"
  tar -xzf "$D/rockyou.txt.tar.gz" -C "$D" && rm -f "$D/rockyou.txt.tar.gz"
fi
fetch xato-1M-passwords.txt "$S/Passwords/Common-Credentials/xato-net-10-million-passwords-1000000.txt"
fetch directory-list-2.3-medium.txt "$S/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt" || \
  fetch directory-list-2.3-medium.txt "$S/Discovery/Web-Content/directory-list-2.3-medium.txt"
fetch raft-large-files.txt "$S/Discovery/Web-Content/raft-large-files.txt"
fetch raft-large-directories.txt "$S/Discovery/Web-Content/raft-large-directories.txt"
fetch subdomains-top110000.txt "$S/Discovery/DNS/subdomains-top1million-110000.txt"
fetch xato-usernames-top.txt "$S/Usernames/xato-net-10-million-usernames.txt"
echo "[+] done -> $D"
ls -lh "$D"
