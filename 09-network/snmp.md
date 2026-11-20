# SNMP (UDP 161)

SNMP v1/v2c authenticates with a **community string** sent in cleartext; defaults `public` (read)
and `private` (read-write). A walk dumps system info, interfaces, processes, installed software,
users, and custom (enterprise) trees. Hint "a port that talks to anyone who knocks — walk it".

## 1. Find it
```bash
sudo nmap -sU -p 161 --script snmp-info <host>
sudo nmap -sU -p 161 --script snmp-brute <host>                # community brute
onesixtyone -c wordlists/network/snmp-communities.txt <host>   # fast community guessing
```
Non-standard port in the lab: `snmp1.chal.deti:8024/udp` → use `host:port` syntax.

## 2. Walk
```bash
snmpwalk -v2c -c public snmp1.chal.deti:8024 1.3.6.1          # everything
snmpwalk -v2c -c public -On host:8024 1.3.6.1.4.1             # enterprise/private tree (custom data!)
snmpbulkwalk -v2c -c public host:8024 .                       # faster
snmpget -v2c -c public host:8024 1.3.6.1.4.1.99999.1.1.0      # one OID
snmp-check -p 8024 -c public host                             # pretty report
snmpwalk ... | grep -o 'flag{[^}]*}'
```
No net-snmp tools? `python scripts/network/snmp_walk.py host:8024 -c public` (pure-Python, no deps).

## Useful OIDs
| OID | Data |
|---|---|
| `1.3.6.1.2.1.1` | system (sysDescr, sysContact, sysName, sysLocation) |
| `1.3.6.1.2.1.2` | interfaces |
| `1.3.6.1.2.1.25.4.2.1.2` / `.5` | running processes / their args (passwords in cmdlines!) |
| `1.3.6.1.2.1.25.6.3.1.2` | installed software |
| `1.3.6.1.4.1.77.1.2.25` | Windows users |
| `1.3.6.1.4.1.*` | vendor/custom — **NET-SNMP-EXTEND / script output** (`1.3.6.1.4.1.8072.1.3`) |

## Write access (`private`)
`snmpset` can change values; NET-SNMP-EXTEND-MIB lets you add a command → RCE.

Seen in: `snmp1` (v2c `public`, flag = output of a status script at `1.3.6.1.4.1.99999.1.1.0`).
