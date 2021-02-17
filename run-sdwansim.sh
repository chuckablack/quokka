ip=$(hostname -I)
echo starting sdwan-sim with host IP address: ${ip}
cd ~/quokka
python3 sdwan-sim/sim_main.py -quokka=${ip}
