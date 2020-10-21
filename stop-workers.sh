ps -ef | grep capture_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
ps -ef | grep portscan_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
ps -ef | grep traceroute_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
