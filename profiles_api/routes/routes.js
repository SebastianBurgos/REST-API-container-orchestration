import express from "../node_modules/express/index.js";
import { getAllProfiles, getProfile, createProfile, updateProfile } from "../controllers/profileController.js";
const router = express.Router()

// ----------------------- Rutas -----------------------
router.get('/profiles', getAllProfiles)
router.get('/profiles/:id', getProfile)
router.post('/profiles', createProfile)
router.put('/profiles/:id', updateProfile)

export default router