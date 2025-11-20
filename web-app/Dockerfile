# spearmint/web-app/Dockerfile

# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /sdk/typescript
COPY sdk/typescript .
# Install SDK dependencies and attempt build (ignoring strict TS errors in generated code)
RUN npm install && (npm run build || true)

WORKDIR /app

# Copy package files
COPY web-app/package.json web-app/package-lock.json ./

# Install Web App dependencies
RUN npm install

# Copy source code
COPY web-app/ .

# Build the static site
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY web-app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]