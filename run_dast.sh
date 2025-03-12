#!/bin/bash

TARGET_URL="http://localhost"
ZAP_PATH="/usr/bin/zaproxy"

echo "Starting OWASP ZAP Security Scan..."
$ZAP_PATH -daemon -host 127.0.0.1 -port 8080 &

# Tunggu ZAP berjalan
sleep 30

echo "Running ZAP Active Scan on: $TARGET_URL"
curl "http://127.0.0.1:8080/JSON/ascan/action/scan/?url=$TARGET_URL&recurse=true&inScopeOnly=false"

# Tunggu hingga scan selesai
sleep 60

# Unduh laporan dalam format HTML
curl "http://127.0.0.1:8080/OTHER/core/other/htmlreport/" -o dast_report.html

echo "DAST Scan Completed! Report saved as dast_report.html"
