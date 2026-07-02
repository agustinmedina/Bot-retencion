# --- Etapa 1: build ---
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- Etapa 2: servir con nginx ---
FROM nginx:alpine

# Angular 17+ genera dist/<nombre-proyecto>/browser
COPY --from=build /app/dist/frontend_analisis/browser /usr/share/nginx/html

COPY nginx.conf.template /etc/nginx/templates/default.conf.template

ENV PORT=80
EXPOSE 80

# La imagen oficial de nginx procesa automáticamente los archivos en
# /etc/nginx/templates/*.template con envsubst antes de arrancar,
# reemplazando ${PORT} por el puerto que Railway inyecte en runtime.
CMD ["nginx", "-g", "daemon off;"]
