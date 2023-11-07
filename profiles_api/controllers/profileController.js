import conexion from "../database/db.js";

export const getAllProfiles = async (req, res) => {
    try {
        const query = `
            SELECT * FROM Perfil
        `;

        const results = await new Promise((resolve, reject) => {
            conexion.query(query, (error, results) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(results);
                }
            });
        });

        return res.json(results);
    } catch (error) {
        return res.json(error);
    }
}

export const getProfile = async (req, res) => {
    try {
        const id = req.params.id;
        conexion.query('SELECT * FROM Perfil WHERE id = ?', [id], async (error, results) => {
            if (error) {
                return res.json(error);
            } else {
                return res.json(results);
            }
        })
    } catch (error) {
        return res.json(error);
    }
}