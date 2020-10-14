cd ~/quokka
./run-quokka.sh &
./run-ui.sh &
./run-sdwansim.sh &./
sudo python3 quokka/workers/capture_worker.py &
sudo python3 quokka/workers/portscan_worker.py &
