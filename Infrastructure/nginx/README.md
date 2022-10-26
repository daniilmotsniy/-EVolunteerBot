# The single entrypoint to start the HelpUkraine service  

## Cloning the repo  
### From 0  
To clone this repository with all the dependent repositories.  
`git clone --recurse-submodules git@github.com:daniilmotsniy/HelpServiceNginx.git`  
### When the "HelpServiceNginx" repo is cloned already  
Initialize the git submodules and fetch the sumbodule repositories content.  
`git submodule init`  
`git submodule update --recursive --remote`  
### Fetching the changes  
To fetch the latest changes in all the submodules repos.  
`git submodule update --remote`  


## Set Up  
### .env for PROD  
To use the PROD version copy `.env.dev` into `.env.prod` and make PROD-dependent updates in `.env.prod`  


## Start the services  
### Docker-compose files  
DEV docker-compose file: `docker-compose.dev.yaml`  
PROD docker-compose file: `docker-compose.yaml`  
### Starting the services set  
#### DEV  
`docker-compose.dev.yaml` is the DEV docker-compose file.  
`docker-compose -f docker-compose.dev.yaml build` to [re]build the services  
`docker-compose -f docker-compose.dev.yaml up`  
#### PROD
Use `docker-compose.yaml` for PROD.  
`docker-compose build` to [re]build the services  
`docker-compose up`  
### Stop the services  
`docker-compose -f docker-compose.dev.yaml down`  