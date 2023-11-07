import express from "express";
import { getAllProfiles, getProfile } from "../controllers/profileController.js";
const router = express.Router()

// ----------------------- Rutas -----------------------
router.get('/perfiles', getAllProfiles)
router.get('/perfiles/:id', getProfile)

export default router