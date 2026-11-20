# Clients for other network services

```bash
ftp host                              # user: anonymous / pass: anonymous ; `ls -la`, `get file`, `binary`
smbclient -L //host -N                # list shares, null session
smbclient //host/share -N             # connect; `ls`, `get file`, `recurse; prompt; mget *`
enum4linux -a host                    # users, shares, policies (SMB/RPC)
dig axfr @host domain.tld             # DNS zone transfer
mysql -h host -u root -p              # MySQL ; psql -h host -U postgres ; redis-cli -h host
smtp-user-enum -M VRFY -U users.txt -t host
ssh user@host -p 22 -v                # banner/version; -i key for found private keys
showmount -e host                     # NFS exports
```
See [09-network](../09-network/README.md) for what to look for on each.
