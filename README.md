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
     -- Shut down your VM 
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
  
## Step 7 Install Docker, Docker CLI, Containerd

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

## Step 9 Create Docker Compose configuration file 

- Create a ' docker-compose.yml' file with the following content:
 - '''' bash
  -- cd docker-project
  -- touch docker-compose.yml
  -- nano docker-compose.yml
 - '''' yaml
 - define the version for docker compose
   version: '3.8'
 - define the services ( for this example we are creating a postgre database and rest api)
  services:
    db:
      image: postgres:latest
      environment:
        POSTGRES_DB: zeyaddatabase
        POSTGRES_USER: zeyaddd
        POSTGRES_PASSWORD: mypasswordz
      volumes:
        - postgres_data:/var/lib/postgresql/data
      networks:
        - mynetwork

    api:
      build: ./api
      depends_on:
        - db
      environment:
        DATABASE_URL: postgres://zeyaddd:mypasswordz@db:5432/zeyaddatabase
      ports:
        - "5000:5000"
      networks:
        - mynetwork
- defining the volumes that can be shared across multiple services or used for presistent storage

  volumes:
    postgres_data:

-defining custom networks for the services to comunicat
  networks:
    mynetwork:




# Step 10 create Custom Dockerfile for API service in api folder


- go back to test-repo
- make a new directory and call it api
 - '''' bash
  -- mkdir api
  -- cd api
- now create the dockerfile 
 -''''bash
 -- touch Dockerfile
- now in that docker file write the python code that will be used to build and reproduce the environment 
 - ''''python
 -- FROM python:3.8-slim

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip install -r requirements.txt

    COPY . .

    CMD ["python", "app.py"]



## Step 11 Create the API application in api folder

- make sure you are in the api directory within the repo
 -''''bash
 -- pwd (lets you know where exactly are you)

- once you confirm you are in the api folder go ahead and create the requirement file
 -'''' bash
 -- touch requirements.txt
 -- nano requirements.txt
- write the following libaries 
Flask
SQLAlchemy
psycopg2-binary


- save then go back to api directory 
- create the app.py file that will serve as the main entry point for the web app

 -'''bash
 -- touch app.py
 -- nano app.py
 -'''' python
- imports to build the app 
 from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

- application set up

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

- model definition

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

- routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price}), 201

- run the application

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
- save file and exit





























 
