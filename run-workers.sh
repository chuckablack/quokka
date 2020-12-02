cd ~/quokka
sudo python3 quokka/workers/quokka_worker.py -H 30 -W capture -Q 192.168.254.34 -S 111-111-112 &
sudo python3 quokka/workers/quokka_worker.py -H 30 -W portscan -Q 192.168.254.34 -S 111-111-112 &
sudo python3 quokka/workers/quokka_worker.py -H 30 -W traceroute -Q 192.168.254.34 -S 111-111-112 &
