# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

### How to run&test the project
* `EXPORT FLASK_APP=api.py`, then `flask run --reload` will start the server
* In Autho0, set up the Application and Api, remember to use the code flow format to get the token and test in postman with Authorization in Bearer token mode.

### Auth0 Authorize Link
The complete documentation for the authorization code flow can be found in [Auth0's Documentation](https://auth0.com/docs/api/authentication#authorize-application). It may help to fill in the url in the textbox below before copying it into your browser:

`https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}`



### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
