# Dockerfile to serve the [dev|prod] Help UA app

FROM node:17.8-alpine3.14

WORKDIR /app

# Add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts -g

# Add the application files
COPY . ./

# Start the development server
CMD ["npm", "start"]