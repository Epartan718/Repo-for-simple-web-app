# This document explain the steps and methods that I have used in order to accomplish the goal of  Deploying a simple application using Docker Compose, consisting of two services:
a REST API and a PostgreSQL database. The API will enable retrieving and adding products through HTTP GET and POST requests


## Step 1 download and install Oracle VM Virtual Box 
 - Download Oracle Virtual Box from this link https://www.virtualbox.org/wiki/Download
 - Set up and install the oracle VM Virtual Box

## Step 2 download the distro you would like to use as a test environment
 
 - I choose to use Centos stream 9 and I Downloaded it through this link https://www.centos.org/download/
 - After I downloaded it the distro I set up a new virtual machine on the virtual box
 - Start the vm and go through the set up and installation process until you get to the home screen
 - Diromg the set up proccess make sure to remmber the ID and Password

## Step 3 install Putty to access your test environment

 - While the installation is working go ahead and install Putty client to ssh to the VM from you computer 
 - You install putty through this client https://www.putty.org/
 - Install putty and set it up
 - we will come back to use putty in a later step

## Step 4 update VM and configure ssh access

 - Update Centos VM 
    - '''' bash 
    -- sudo dnf update -y
 - Once update is complete go ahead, install, start, and enable  SSH
    -  '''' bash
    -- sudo dnf install -y openssh-server
    -- sudo systemctl start sshd
    -- sudo systemctl enable sshd
 - Verify that SSH client is running in the VM
  - '''' bash
    -- sudo systemctl status sshd 

## Step 5 SSH into the instance through the Putty Client

 - find the IP address of the VM 
   - '''' bash
    -- ip addr show 
    -- 192.168.12.233
   - once we obtained the IP address of the instance we will go to Putty Client and ssh into the VM
   - some key pointers to make sure of
     -- make sure the shh option is marker 
     -- make sure it is configured to the default port which is port 22
     -- then open the instance and enter the ID and Password

   - If for any reason you get the error of network connection timeout go through the following steps
     -- Shudont your VM 
     -- Go to VM settings --> Network -> Adapter 1 -> Attached to : Bridged Adapter
     -- Start your VM again.

   - this shoud fix the issue if you got that error



## Step 6 install and configure git  

- Now once you have accessed the instance its time to install and configure git for the documentation of the project
   - '''' bash
    -- sudo dnf install -y git
    -- git --version
    -- git config --global user.name "Epartan718"
    -- git config --global user.email "zeyadelbliety718@hotmail.com"
  
  - Go to GitHub webestie : https://github.com/
  - login to your account
  - create a new repo by clicking "+" 
  - Name your repo
  - create the repository
  - after go to your account settings
  - select developer settings
  - select personal access tokens
  - select Tokens (classic)
  - generate new token (classic)
  - name it 
  - then select all the admin options
  - then click generate token
  -  keep the password on a different tap for we will use it later

 - now we will clone the repository 
 - '''' bash 
   -- git clone https://github.com/Epartan718/test-repo.git
   -- cd test-repo
   -- touch README.md
  
## Step 7 Install Docker, Docker CLI, Continerd

- so we will find install dnf package manager in order to install docker
 - '''' bash
 -- sudo dnf update -y 
 -- sudo dnf install -y dnf-plugins-core
- Add Docker repo 
 - '''' bash
 -- sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
- Install Docker CE
 -- sudo dnf install -y docker-ce docker-ce-cli containerd.io
- start and enable Docker
 -- sudo systemctl start docker
 -- sudo systemctl enable docker
- verify if docker is working
 -- sudo docker run hello-world

 
## Step 8 Install Docker Compose, Grant premission and verify installation 

- Download docker compose
 - '''' bash
 -- sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 -- sudo chmod +x /usr/local/bin/docker-compose
 -- docker-compose -- version



































 
