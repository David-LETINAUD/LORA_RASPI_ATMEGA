# Configurer gateway comme un service
sudo cp gateway.service /lib/systemd/system/  
sudo chmod 644 /lib/systemd/system/gateway.service  
chmod +x /home/pi/Desktop/gateway/gateway.py  
  
sudo systemctl daemon-reload  
sudo systemctl enable gateway.service  
sudo systemctl start gateway.service  

# Commandes utiles
## Check status  
sudo service gateway status
 
## Start service  
sudo service gateway start  
 
## Stop service  
sudo service gateway stop  
 
## Check service's log  
sudo journalctl -f -u gateway.service  
