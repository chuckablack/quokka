cd ~/quokka
sudo python3 quokka/workers/quokka_worker.py -H 5 -W capture -Q localhost -S 111-111-111 -C http &
sudo python3 quokka/workers/quokka_worker.py -H 5 -W portscan -Q localhost -S 111-111-111 -C http &
sudo python3 quokka/workers/quokka_worker.py -H 5 -W traceroute -Q localhost -S 111-111-111 -C http &
