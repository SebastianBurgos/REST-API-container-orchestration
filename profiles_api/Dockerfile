# Usa una imagen de Node.js en su versión "alpine"
FROM node:alpine

# Establece el directorio de trabajo en la imagen
WORKDIR /app

# Establecer la carpeta node_modules y sus permisos
RUN mkdir -p ./node_modules && chown -R node:node ./

# Copia los archivos package.json y package-lock.json
COPY package*.json ./

# Declarar el usuario node
USER node

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos de la aplicación
COPY --chown=node:node . .

# Expón el puerto en el que se ejecuta tu aplicación
EXPOSE 4000

# Define el comando para iniciar la aplicación
CMD ["node", "api_perfiles.js"]
