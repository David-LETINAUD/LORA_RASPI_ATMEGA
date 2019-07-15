cp gateway.service /lib/systemd/system/  
sudo chmod 644 /lib/systemd/system/gateway.service  
chmod +x /home/pi/Desktop/gateway/gateway.py  
  
sudo systemctl daemon-reload  
sudo systemctl enable gateway.service  
sudo systemctl start gateway.service  


'## Check status  
sudo systemctl status gateway.service  
 
'## Start service  
sudo systemctl start gateway.service  
 
'## Stop service  
sudo systemctl stop gateway.service  
 
'## Check service's log  
sudo journalctl -f -u gateway.service  
