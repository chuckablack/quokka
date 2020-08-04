pkill flask
pkill node
ps -ef | grep sim_main | grep -v grep | awk '{print $2}' | xargs kill
