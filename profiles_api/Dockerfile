# Usa una imagen de Node.js en su versión "alpine"
FROM node:alpine

# Establece el directorio de trabajo en la imagen
WORKDIR /app

# Copia los archivos package.json y package-lock.json
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos de la aplicación
COPY . .

# Expón el puerto en el que se ejecuta tu aplicación
EXPOSE 4000

# Define el comando para iniciar la aplicación
CMD ["node", "api_perfiles.js"]
