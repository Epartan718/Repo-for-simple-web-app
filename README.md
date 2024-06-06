# This document explain the steps and methods that I have used in order to accomplish the goal of  Deploying a simple application using Docker Compose, consisting of two services:
a REST API and a PostgreSQL database. The API will enable retrieving and adding products through HTTP GET and POST requests


## Step 1 download and install Oracle VM Virtual Box 
 - Download Oracle Virtual Box from this link https://www.virtualbox.org/wiki/Download
 - Set up and install the oracle VM Virtual Box

## Step 2 download the distro you would like to use as a test environment
 
 - I choose to use Centos stream 9 and I Downloaded it through this link https://www.centos.org/download/
 - After I downloaded it the distro I set up a new virtual machine on the virtual box
 - Start the vm and go through the set up and installation process until you get to the home screen
 - During the set up proccess make sure to remmber the ID and Password

## Step 3 install Putty to access your test environment

 - While the installation is working go ahead and install Putty client to ssh to the VM from you computer 
 - You install putty through this client https://www.putty.org/
 - Install putty and set it up
 - we will come back to use putty in a later step

## Step 4 update VM and configure ssh access


# Update Centos VM 
    -- sudo dnf update -y
# Once update is complete go ahead, install, start, and enable  SSH
    -- sudo dnf install -y openssh-server
    -- sudo systemctl start sshd
    -- sudo systemctl enable sshd
# Verify that SSH client is running in the VM
    -- sudo systemctl status sshd 

## Step 5 SSH into the instance through the Putty Client

# Find the IP address of the VM 
    -- ip addr show 
# Select the ip addresse that is next to inet in enp0s3 sectiom
   - once we obtained the IP address of the instance we will go to Putty Client and ssh into the VM
# Some key pointers to make sure of
     -- make sure the ssh option is marked 
     -- make sure it is configured to the default port which is port 22
     -- then open the instance and enter the ID and Password

# If for any reason you get the error of network connection timeout go through the following steps
     -- Shut down your VM 
     -- Go to VM settings --> Network -> Adapter 1 -> Attached to : Bridged Adapter
     -- Start your VM again.

# This shoud fix the issue if you got that error



## Step 6 install and configure git
  
#Now once you have accessed the instance its time to install and configure git for the documentation of the project
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
# Keep the password on a different tap for we will use it later

# Now we will clone the repository  
   -- git clone https://github.com/Epartan718/test-repo.git
   -- cd test-repo
   -- touch README.md
# Update README.md file as you go to give guidance for anyone who would like to create the application
  

## Step 7 Install Docker, Docker CLI, Containerd

# So we will find install dnf package manager in order to install docker
 -- sudo dnf update -y 
 -- sudo dnf install -y dnf-plugins-core
# Add Docker repo 
 -- sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# Install Docker CE
 -- sudo dnf install -y docker-ce docker-ce-cli containerd.io
# Start and enable Docker
 -- sudo systemctl start docker
 -- sudo systemctl enable docker
# Verify if docker is working
 -- sudo docker run hello-world

 
## Step 8 Install Docker Compose, Grant premission and verify installation 

# Download docker compose
 -- sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 -- sudo chmod +x /usr/local/bin/docker-compose
 -- docker-compose -- version

## Step 9 Create Docker Compose configuration file 

# Create a docker-compose.yml file with the following content:
  -- cd docker-project
  -- touch docker-compose.yml
  -- vim docker-compose.yml

 - ''' yml
version: '3.8'

services:
  db:
# Using the latest version of the official PostgreSQL image
    image: postgres:latest
    environment:
# Setting environment variables for PostgreSQL database
      POSTGRES_DB: zeyaddatabase
      POSTGRES_USER: zeyaddd
      POSTGRES_PASSWORD: mypasswordz
    volumes:
# Persisting PostgreSQL data in a named volume
      - postgres_data:/var/lib/postgresql/data
    networks:
# Connecting the database to a custom network
      - mynetwork

  api:
# Building the API service from the Dockerfile in the 'api' directory
    build: ./api
    depends_on:
# Ensuring the database service starts before the API service
      - db
    environment:
# Setting environment variable for the database URL
      DATABASE_URL: postgresql://zeyaddd:mypasswordz@db:5432/zeyaddatabase
    ports:
# Mapping port 5000 on the host to port 5000 in the container
      - "5000:5000"
    networks:
# Connecting the API service to the custom network
      - mynetwork

volumes:
# Defining a named volume for persisting PostgreSQL data
  postgres_data:

networks:
# Defining a custom network for the services
  mynetwork:

'''
 
# Step 10 create Custom Dockerfile for API service in api folder

# Make a new directory and call it api
  -- mkdir api
  -- cd api
# Now create the dockerfile 
 -- touch Dockerfile
 -- vim Dockerfile


# Now in that docker file write the python code that will be used to build and reproduce the environment 
 
 - '''python

# Using a slim version of the official Python 3.8 image
FROM python:3.8-slim

# Installing necessary packages and dependencies
RUN apt-get update && apt-get install -y python3-pip libpq-dev gcc

# Setting the working directory inside the container
WORKDIR /app

# Copying the requirements file to the container
COPY requirements.txt .

# Installing Python dependencies
RUN pip install -r requirements.txt

# Copying the rest of the application code to the container
COPY . .

# Command to run the application
CMD ["python", "app.py"]

'''

## Step 11 Create the API application in api folder

# Make sure you are in the api directory within the repo
-- pwd

# Once you confirm you are in the api folder go ahead and create the requirement file
 -- touch requirements.txt
 -- vim requirements.txt

# Write the following libaries 

# Flask web framework for building the API
Flask
# PostgreSQL adapter for Python
psycopg2-binary
# Extension for Flask to support SQLAlchemy
Flask-sqlalchemy


#Save then go back to api directory
 
# Create the app.py file that will serve as the main entry point for the web app
 -- touch app.py
 -- vim app.py

 -''' pytho
n
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application")

# Configuring the SQLAlchemy part of Flask
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Routes
@app.route('/products', methods=['GET'])
def get_products():
# Querying all products from the database
    products = Product.query.all()
# Formatting the products for JSON response
    formatted_products = [
        {'id': p.id, 'name': p.name, 'price': p.price} for p in products
    ]
# Returning the formatted products and the total count
    return jsonify({
        'products': formatted_products,
        'total': len(formatted_products)
    })

@app.route('/products', methods=['POST'])
def add_product():
# Getting the JSON data from the request
    data = request.get_json()


# Validating input data
    if not data or not 'name' in data or not 'price' in data:
        abort(400, description="Request must contain 'name' and 'price' fields")

    try:
# Creating a new product instance
        new_product = Product(name=data['name'], price=float(data['price']))
        db.session.add(new_product)
        db.session.commit()
    except (ValueError, TypeError):
        abort(400, description="Invalid input data format")

# Returning the created product
    return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price}), 201

# Initialize database and add initial products
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Adding initial products if not already present
        initial_products = [
            {"name": "Ice Cream", "price": 5.99},
            {"name": "Chocolate", "price": 3.99},
            {"name": "Fruits", "price": 4.99}
        ]

        for product_data in initial_products:
            if not Product.query.filter_by(name=product_data["name"]).first():
                product = Product(name=product_data["name"], price=product_data["price"])
                db.session.add(product)
        db.session.commit()

    # Running the Flask application
    app.run(host='0.0.0.0', port=5000)
'''
# Save then exit file


## Step 12 Build the Dockercompose image 

# Head to the project root 
-- cd ..


# Build and start the Docker compose
-- docker-compose up --build 

# Verify if the image is up 
-- docker-compose ps




## Step 13 Test the functionality of the Api


- Use the following tests to verify the full functionality of the api 

# Test GET /products Endpoint
-- curl -X GET http://localhost:5000/products

# Test POST /products Endpoint
-- curl -X POST -H "Content-Type: application/json" -d '{"name":"Ice Cream","price":5.99}' http://localhost:5000/products

# Verify the New Product was added 
-- curl -X GET http://localhost:5000/products

# Add more products 
-- curl -X POST -H "Content-Type: application/json" -d '{"name":"Banana","price":3.99}' http://localhost:5000/products

-- curl -X POST -H "Content-Type: application/json" -d '{"name":"Chips","price":2.99}' http://localhost:5000/products

# Verify if all products were added
--curl -X GET http://localhost:5000/products

# Test for missin name or price 
-- curl -X POST -H "Content-Type: application/json" -d '{"price":5.99}' http://localhost:5000/products
-- curl -X POST -H "Content-Type: application/json" -d '{"name":"Ice Cream"}' http://localhost:5000/products

# Test for invalid price format
 -- curl -X POST -H "Content-Type: application/json" -d '{"name":"Ice Cream","price":"invalid"}' http://localhost:5000/products




# Step 14 Final

- After playing around and exploring the environment you can go ahead and shut down everthingy by using the following

# Stop running containers
-- docker-compose down

# Additional clean up 
-- docker volume prune -f
-- docker network prune -f
-- docker image prune -f

# Shutdown VM
-- Sudo shutdown now


#Thank you so much for allowing me to take part in this project I enjoyed every moment working on it!!


