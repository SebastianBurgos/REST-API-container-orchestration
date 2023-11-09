# Usa una imagen de Node.js en su versión "alpine"
FROM node:alpine

# Establecer la carpeta node_modules y sus permisos
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

# Establece el directorio de trabajo en la imagen
WORKDIR /home/node/app

# Copia los archivos package.json y package-lock.json
COPY package*.json ./

# Declarar el usuario node
USER node

# Instala las dependencias
RUN npm ci

# Copia el resto de los archivos de la aplicación
COPY --chown=node:node . .

# Expón el puerto en el que se ejecuta tu aplicación
EXPOSE 4000

# Define el comando para iniciar la aplicación
CMD ["node", "api_perfiles.js"]
