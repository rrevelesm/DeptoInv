# 📤 Guía para Subir el Proyecto a GitHub

## Tu Repositorio: https://github.com/rrevelesm/DeptoInv_UPIIZ

---

## 🔧 PASO 1: Instalar Git (Si no lo tienes)

### Descargar Git para Windows

1. Ve a: https://git-scm.com/download/win
2. Descarga la versión de 64 bits
3. Ejecuta el instalador
4. Deja todas las opciones por defecto (Next, Next, Next...)
5. **IMPORTANTE:** Reinicia PowerShell o la terminal después de instalar

### Verificar instalación

```powershell
git --version
```

Debe mostrar algo como: `git version 2.x.x`

---

## 📦 PASO 2: Configurar Git (Primera vez)

```powershell
# Configurar tu nombre
git config --global user.name "Rafael Reveles"

# Configurar tu email (el de GitHub)
git config --global user.email "tu-email@ejemplo.com"
```

---

## 🚀 PASO 3: Subir el Proyecto a GitHub

### Método Automático (Recomendado)

**Ejecuta este comando:**

```powershell
.\subir_github.bat
```

### Método Manual (Si el script no funciona)

```powershell
# 1. Ir a la carpeta del proyecto
cd C:\Users\rafael\Desktop\IDE_Cursor\DeptoInv

# 2. Inicializar Git
git init

# 3. Agregar todos los archivos
git add .

# 4. Crear el primer commit
git commit -m "🎓 Primer commit: Sistema de Gestión de Investigación UPIIZ"

# 5. Renombrar rama principal a 'main'
git branch -M main

# 6. Conectar con tu repositorio de GitHub
git remote add origin https://github.com/rrevelesm/DeptoInv_UPIIZ.git

# 7. Subir los archivos
git push -u origin main
```

**GitHub te pedirá autenticación:**
- Usuario: `rrevelesm`
- Contraseña: Tu **Personal Access Token** (no tu contraseña normal)

---

## 🔑 PASO 4: Crear Personal Access Token (Si es necesario)

Si GitHub te pide una contraseña y no funciona, necesitas un token:

1. Ve a: https://github.com/settings/tokens
2. Clic en "Generate new token" → "Generate new token (classic)"
3. **Nota:** "Token para DeptoInv_UPIIZ"
4. **Expiration:** 90 días (o sin expiración)
5. **Permisos:** Marca solo `repo` (acceso completo a repositorios)
6. Clic en "Generate token"
7. **⚠️ COPIA EL TOKEN** (no lo verás de nuevo)
8. Usa este token como contraseña cuando hagas `git push`

---

## 📋 ¿Qué se va a subir?

### ✅ Archivos que SÍ se subirán:

```
✅ app.py
✅ models.py
✅ database.py
✅ requirements.txt
✅ README.md
✅ LICENSE
✅ .gitignore
✅ static/ (HTML, CSS, JS)
✅ docs/ (todas las guías)
✅ batch/ (scripts .bat)
✅ scripts/ (scripts Python)
✅ Proyectos 2025 Investigación.xlsx
```

### ❌ Archivos que NO se subirán (en .gitignore):

```
❌ investigacion_upiiz.db (base de datos - datos sensibles)
❌ formularios/ (formularios recibidos - datos personales)
❌ __pycache__/ (archivos temporales Python)
❌ venv/ (entorno virtual)
❌ *.log (archivos de log)
```

---

## 🔄 Actualizar el Repositorio (Futuros cambios)

Cuando hagas cambios en el futuro:

```powershell
# 1. Ver qué archivos cambiaron
git status

# 2. Agregar los cambios
git add .

# 3. Hacer commit con un mensaje descriptivo
git commit -m "Descripción de los cambios"

# 4. Subir a GitHub
git push
```

---

## 🌟 PASO 5: Verificar en GitHub

1. Ve a: https://github.com/rrevelesm/DeptoInv_UPIIZ
2. Deberías ver todos los archivos
3. El README.md se mostrará automáticamente
4. ¡Tu proyecto está en línea! 🎉

---

## 🔧 Solución de Problemas

### Error: "git: command not found"

**Solución:** Instalar Git (Paso 1) y reiniciar la terminal

### Error: "Permission denied"

**Solución:** Usar Personal Access Token en lugar de contraseña (Paso 4)

### Error: "Updates were rejected"

**Solución:**
```powershell
git pull origin main --allow-unrelated-histories
git push
```

### Error: "Repository not found"

**Solución:** Verificar que el repositorio sea correcto:
```powershell
git remote -v
# Debe mostrar: https://github.com/rrevelesm/DeptoInv_UPIIZ.git
```

Si está mal, corregir:
```powershell
git remote set-url origin https://github.com/rrevelesm/DeptoInv_UPIIZ.git
```

---

## 📊 Después de Subir a GitHub

### Beneficios:

✅ **Respaldo en la nube** - Tu código está seguro
✅ **Control de versiones** - Historial de todos los cambios
✅ **Colaboración** - Otros pueden ver y colaborar
✅ **Despliegue fácil** - PythonAnywhere puede clonar desde GitHub

### Desplegar en PythonAnywhere desde GitHub:

```bash
# En la consola de PythonAnywhere:
git clone https://github.com/rrevelesm/DeptoInv_UPIIZ.git
cd DeptoInv_UPIIZ
pip3.10 install --user -r requirements.txt
```

Luego seguir el tutorial de PythonAnywhere.

---

## 🎓 Comandos Git Útiles

```powershell
# Ver estado del repositorio
git status

# Ver historial de commits
git log --oneline

# Ver diferencias de archivos
git diff

# Deshacer cambios (antes de commit)
git restore archivo.py

# Crear una rama nueva
git branch nombre-rama
git checkout nombre-rama

# Ver ramas
git branch

# Cambiar de rama
git checkout main
```

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que Git esté instalado: `git --version`
2. Verifica la URL del repositorio: `git remote -v`
3. Intenta el método manual paso por paso
4. Usa Personal Access Token en lugar de contraseña

**GitHub Docs:** https://docs.github.com/es

---

## ✅ Checklist

- [ ] Git instalado y configurado
- [ ] Repositorio inicializado (`git init`)
- [ ] Archivos agregados (`git add .`)
- [ ] Primer commit creado
- [ ] Remote configurado (tu repositorio GitHub)
- [ ] Push exitoso a GitHub
- [ ] Verificado en GitHub web

---

© 2025 UPIIZ - Instituto Politécnico Nacional

