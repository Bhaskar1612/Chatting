# Use the official Node.js 14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the React application
RUN npm run build

# Install serve to serve the build directory
RUN npm install -g serve

# Expose port 3000 to the outside world
EXPOSE 3000

# Command to run the application
CMD ["serve", "-s", "build", "-l", "3000"]
