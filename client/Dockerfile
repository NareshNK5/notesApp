FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Serve static build using a simple server (like serve or nginx)
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "5173"]
