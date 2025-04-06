FROM node:14.8.0-alpine3.12

WORKDIR .

# Copy package files and install dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@3.4.3 -g

# Copy the rest of the application code
COPY . ./

EXPOSE 3000

# Start the application
CMD ["npm", "start"]
