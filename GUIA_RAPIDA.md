# ⚡ Guía Rápida - Padrón de Investigadores UPIIZ

## 🚀 Primera vez en una PC nueva (15 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/rrevelesm/DeptoInv.git
cd DeptoInv

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

---

## 📅 Uso diario (cada vez que trabajes)

### Iniciar trabajo:
```bash
# 1. Actualizar código
git pull origin main

# 2. Iniciar servidor
python app.py
```

### Hacer cambios:
```bash
# Ver en navegador: http://localhost:5000/formulario

# Guardar y subir cambios
git add .
git commit -m "Descripción de cambios"
git push origin main
```

---

## 🔄 Sincronizar entre computadoras

**PC1 (donde trabajaste):**
```bash
git add . ; git commit -m "Cambios" ; git push
```

**PC2 (donde vas a trabajar):**
```bash
git pull
python app.py
```

---

## 📱 Compartir formulario en red local

```bash
# 1. Obtener IP local
ipconfig
# Busca: Dirección IPv4 (ej: 192.168.0.6)

# 2. Compartir URL
http://192.168.0.6:5000/formulario
```

---

## 🛠️ Comandos más usados

```bash
git status                    # Ver cambios
git log --oneline -n 5       # Ver historial
git restore archivo.html     # Descartar cambios
python app.py                # Iniciar servidor
```

---

## 🆘 Problemas comunes

**Puerto ocupado:**
```bash
netstat -ano | findstr :5000
taskkill /PID [número] /F
```

**Git no funciona:**
```bash
$env:Path += ";C:\Program Files\Git\cmd"
```

**Dependencias faltantes:**
```bash
pip install -r requirements.txt
```

---

## 📋 URLs del sistema

- Formulario: http://localhost:5000/formulario
- Panel admin: http://localhost:5000/panel-formularios
- Generar QR: http://localhost:5000/generar-qr

---

**Documentación completa:** Ver `PIPELINE_EJECUCION.md`

