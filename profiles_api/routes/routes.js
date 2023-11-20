import express from "express";
import { getAllProfiles, getProfile, createProfile, updateProfile, deleteProfile } from "../controllers/profileController.js";
const router = express.Router()

// ----------------------- Rutas -----------------------
router.get('/profiles', getAllProfiles)
router.get('/profiles/:id', getProfile)
router.post('/profiles', createProfile)
router.put('/profiles/:id', updateProfile)
router.delete('/profiles/:id', deleteProfile)

export default router