# Bookshop e-commerce app with Razorpay Payment Gateway

A simple Django e-commerce project with the integration of Razorpay payment gateway.

#### Prerequisite

Razorpay merchant account and API credentials. The credentials are saved as environment variables as follows:
RAZORPAY_ID and RAZORPAY_SECRET_KEY.

#### Build and spin up the container
    docker-compose up --build

_The app will run on the port 8005. You may want to change that in the docker compose file._