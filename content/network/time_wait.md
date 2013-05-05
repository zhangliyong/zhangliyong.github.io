Title: TIME_WAIT in netstat


netstat -tanp | grep -o '\(10.18.10.20\|211.151.139.230\|127.0.0.1\):[0-9]*' | sort -nr | uniq -c | sort -nr -k 1 | wc -l
