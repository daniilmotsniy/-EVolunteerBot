The main NginX docker image copy

# Building the Docker image separately
`docker build -t help-ukraine-nginx-ui .`
`docker save help-ukraine-nginx-ui | gzip > help-ukraine-nginx-ui.tar.gz`

`docker load < help-ukraine-nginx-ui.tar.gz`
`docker run -d -p 80:80 help-ukraine-nginx-ui`