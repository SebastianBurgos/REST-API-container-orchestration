import express from "express";
const app = express();

const PORT = process.env.PORT || 4000;

app.use(express.json());

// Rutas
app.get('/perfil', (req, res) => {
    // Aquí puedes enviar la lista de perfiles (dummy data en este ejemplo)
    const perfiles = [
        { id: 1, nombre: 'Juan', edad: 25 },
        { id: 2, nombre: 'María', edad: 30 },
        // Agrega más perfiles si lo deseas
    ];

    res.json(perfiles);
});

app.get('/perfil/:id', (req, res) => {
    const perfilId = req.params.id;
    // Aquí puedes buscar un perfil por su ID (dummy data en este ejemplo)
    const perfil = {
        id: perfilId,
        nombre: 'Nombre Dummy',
        edad: 99,
    };

    res.json(perfil);
});

app.listen(PORT, () => {
    console.log(`Api de perfiles corriendo en el puerto: ${PORT}`);
});