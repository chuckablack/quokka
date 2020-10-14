pkill flask
pkill node
ps -ef | grep sim_main | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep capture_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
ps -ef | grep portscan_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
