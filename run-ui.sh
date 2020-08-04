ip=$(hostname -I)
echo starting quokka-ui with host IP address: ${ip}
sed -i "s/192.168.254.125/${ip}/" quokka-ui/.env
cat quokka-ui/.env
cd ~/quokka/quokka-ui
npm start
