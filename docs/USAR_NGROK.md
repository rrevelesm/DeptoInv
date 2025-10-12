# 🌐 Compartir el Formulario desde Casa con Ngrok

## ¿Qué es Ngrok?

Ngrok crea un **túnel público** a tu computadora, permitiendo que cualquier persona con internet acceda a tu formulario, **incluso si no están en tu red**.

---

## 🚀 Instalación de Ngrok

### Paso 1: Descargar Ngrok

1. Ve a: https://ngrok.com/download
2. Descarga la versión para Windows
3. Descomprime el archivo `ngrok.exe` en tu carpeta `DeptoInv`

---

## 📋 Uso Rápido

### Paso 1: Iniciar tu servidor Flask

```bash
python app.py
```

Déjalo corriendo (verás `Running on http://127.0.0.1:5000`)

### Paso 2: En OTRA terminal, ejecutar Ngrok

```bash
ngrok http 5000
```

### Paso 3: Copiar la URL pública

Verás algo como:

```
ngrok by @inconshreveable

Session Status                online
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
Forwarding                    http://abc123.ngrok.io -> http://localhost:5000

Connections                   0

Press Ctrl+C to stop
```

### Paso 4: Compartir con Investigadores

La URL que debes compartir es:

```
https://abc123.ngrok.io/formulario
```

**⚠️ IMPORTANTE:**
- La URL cambia CADA VEZ que reinicias ngrok
- La sesión gratuita dura 2 horas
- Tu computadora DEBE estar encendida

---

## 🎯 Ventajas de Ngrok

✅ Los investigadores pueden acceder desde **cualquier lugar**
✅ Funciona desde **cualquier dispositivo** (PC, celular, tablet)
✅ Funciona con **cualquier red** (WiFi casa, datos móviles, etc.)
✅ Es **gratuito** para uso básico
✅ Tiene **HTTPS** (seguro)

---

## ⚠️ Desventajas de Ngrok (Gratis)

❌ La URL cambia cada vez que reinicias
❌ Sesión expira después de 2 horas
❌ Tienes que dejar tu PC encendida
❌ Ancho de banda limitado

---

## 💎 Ngrok Premium (Opcional)

Si creas cuenta en ngrok.com:

✅ URLs personalizadas que no cambian
✅ Sin límite de tiempo
✅ Más conexiones simultáneas

**Costo:** ~$8 USD/mes

---

## 📱 Ejemplo de Mensaje para Investigadores

```
Estimado(a) investigador(a):

Favor de llenar el siguiente formulario:

🔗 https://abc123.ngrok.io/formulario

Importante: Este link estará activo hasta [FECHA/HORA]

Departamento de Investigación - UPIIZ
M. en C. Rafael Reveles Martínez
```

---

## 🛠️ Script Automatizado

He creado un script para facilitar el proceso:

```batch
iniciar_con_ngrok.bat
```

Este script:
1. Inicia el servidor Flask
2. Inicia Ngrok automáticamente
3. Te muestra la URL pública

---

## 🔍 Solución de Problemas

### "ngrok: command not found"

**Solución:** Asegúrate de que `ngrok.exe` esté en la carpeta actual o en tu PATH

### "Failed to listen on localhost:5000"

**Solución:** El puerto 5000 ya está en uso. Mata el proceso:

```powershell
Get-Process -Name python | Stop-Process -Force
```

---

## 📞 Soporte

Departamento de Investigación - UPIIZ
M. en C. Rafael Reveles Martínez
investigacion_UPIIZ@ipn.mx

© 2025 UPIIZ - IPN

