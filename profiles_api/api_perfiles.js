import express from "express";
import router from "./routes/routes.js";
const app = express();

// Definir el puerto
const PORT = 4000;

// Para usar peticiones y respuestas en formato JSON
app.use(express.json());

//llamar al router
app.use('/', router)

app.listen(PORT, () => {
    console.log(`Api de perfiles corriendo en el puerto: ${PORT}`);
});