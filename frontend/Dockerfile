# Use official Node.js 20 image
FROM node:24-slim

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port 3000 for Vite
EXPOSE 3000

# Command to run the development server
CMD ["npm", "run", "dev"]
# CMD ["npm", "run", "dev"]