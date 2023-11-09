import express from "express";
import { getAllProfiles, getProfile, updateProfile } from "../controllers/profileController.js";
const router = express.Router()

// ----------------------- Rutas -----------------------
router.get('/perfiles', getAllProfiles)
router.get('/perfiles/:id', getProfile)
router.put('/perfiles/:id', updateProfile)

export default router