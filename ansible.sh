
sudo rm -rf hosts
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
pip install pywinrm[credssp]
 ansible all -m win_ping
sudo cp /Users/rikenpatel/Downloads/SQLSERVER_ANSIBLE_DEPLOYMENT.yaml /etc/ansible/playbooks

ansible-playbook -i /etc/ansible/hosts SQLSERVER_ANSIBLE_DEPLOYMENT.yaml --tags Dir_Structures --limit 172.23.102.80
ansible-playbook -i /etc/ansible/hosts SQLSERVER_ANSIBLE_DEPLOYMENT.yaml --tags Dir_Structures,Foldercopy,SSMS,SQLSERVER,SQLSCRIPTS,CU --limit  172.23.102.80


sudo cp /Users/rikenpatel/Downloads/SQLSERVER_ANSIBLE_DEPLOYMENT.yaml /etc/ansible/playbooks
sudo cp /etc/ansible/playbooks/SQLSERVER_ANSIBLE_DEPLOYMENT.yaml /Users/rikenpatel/Downloads/SQLSERVER_ANSIBLE_DEPLOYMENT_1.yaml