FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.env ./     
COPY --from=builder /app/dist ./dist 
COPY --from=builder /app/index.js ./  

EXPOSE 3000

CMD ["npm", "start"]