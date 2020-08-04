ip=$(hostname -I)
echo starting quokka-ui with host IP address: ${ip}
sed -i "s/<quokka-ip>/${ip}/" quokka-ui/.env
cat quokka-ui/.env
cd ~/quokka/quokka-ui
npm start
sed -i "s/${ip}/<quokka-ip>/" .env
cat .env
