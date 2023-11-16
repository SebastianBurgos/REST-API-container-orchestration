import express from "express";
import router from "./routes/routes.js";
import { consumeMessages } from "./controllers/automatizedProfileEvent.js";
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

// Iniciar proceso consumidor de eventos para la creacion automatica de los profiles
consumeMessages().catch((error) => {
    console.error('Error al iniciar consumeMessages:', error);
    server.close();
});