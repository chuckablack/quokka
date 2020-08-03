ip=$(hostname -I)
ip = `echo $ip | sed "s/ //"`
sed -i "s/192.168.254.114/${ip}/" quokka/sim/sim_main.py
python3 quokka/sim/sim_main.py
