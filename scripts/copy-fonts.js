import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const rootDir = path.resolve(__dirname, '..')

// Create fonts directory if it doesn't exist
const fontsDir = path.resolve(rootDir, 'core/static/fonts')
if (!fs.existsSync(fontsDir)) {
  fs.mkdirSync(fontsDir, { recursive: true })
}

// Copy bootstrap-icons fonts
const bootstrapIconsDir = path.resolve(rootDir, 'node_modules/bootstrap-icons/font/fonts')
fs.readdirSync(bootstrapIconsDir).forEach(file => {
  fs.copyFileSync(
    path.resolve(bootstrapIconsDir, file),
    path.resolve(fontsDir, file)
  )
})

console.log('✅ Fonts copied successfully') 