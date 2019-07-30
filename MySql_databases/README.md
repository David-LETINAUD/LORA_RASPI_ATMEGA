# Mysql databases  
## Création user  
sudo mysql -u root -p  
GRANT ALL PRIVILEGES ON '*.*' TO 'username'@'%' IDENTIFIED BY 'password';  

Avec '%' connexion à distance autorisée    
