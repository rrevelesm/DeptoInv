# 🌐 Guía para Compartir el Formulario de Investigadores

**UPIIZ - Departamento de Investigación**  
M. en C. Rafael Reveles Martínez

---

## 📍 Tu Dirección IP Local: **192.168.0.4**

---

## 🚀 PASO 1: Iniciar el Servidor en Modo Red

### Opción A: Script Automático (Recomendado) ⭐

```batch
iniciar_sistema_red.bat
```

### Opción B: Manual

```bash
python app.py
```

**Verás en la consola:**
```
* Running on http://0.0.0.0:5000
* Running on http://192.168.0.4:5000  ← Esta es tu dirección
```

---

## 📋 PASO 2: Compartir el Formulario con Investigadores

### 🌐 URL del Formulario para Investigadores:

```
http://192.168.0.4:5000/formulario
```

### 📧 Cómo Compartir:

**Por Email:**
```
Estimado(a) investigador(a):

Favor de llenar el siguiente formulario de actualización de datos:

🔗 http://192.168.0.4:5000/formulario

Departamento de Investigación - UPIIZ
M. en C. Rafael Reveles Martínez
```

**Por WhatsApp/Mensaje:**
```
Favor de llenar el formulario de investigadores en:
http://192.168.0.4:5000/formulario

Depto. Investigación - UPIIZ
```

**QR Code:**
- Genera un código QR con esta URL
- Imprímelo o compártelo digitalmente
- Los investigadores lo escanean con su celular

---

## ✅ REQUISITOS IMPORTANTES

### Para que Funcione en Red Local:

1. **Tu computadora debe estar ENCENDIDA** mientras los investigadores llenen el formulario
2. **Todos deben estar en la MISMA red WiFi/LAN**
   - Red: WiFi institucional UPIIZ
   - Tu IP: 192.168.0.4
3. **Firewall de Windows:**
   - Debe permitir Python en la red local
   - (El sistema te preguntará al iniciar)

### Verificación:

**En tu computadora:**
```
http://localhost:5000/formulario  ← Debe funcionar
```

**Desde otra computadora en la red:**
```
http://192.168.0.4:5000/formulario  ← Debe funcionar
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Problema 1: "No se puede acceder al sitio" desde otra PC

**Causa:** Firewall de Windows bloqueando

**Solución:**
1. Panel de Control → Firewall de Windows
2. Configuración Avanzada → Reglas de Entrada
3. Nueva Regla → Puerto → TCP → 5000
4. Permitir conexión en redes de dominio y privadas

**O simplemente:**
```powershell
netsh advfirewall firewall add rule name="Flask UPIIZ" dir=in action=allow protocol=TCP localport=5000
```

### Problema 2: La IP cambió

**Tu IP puede cambiar si:**
- Reinicias la computadora
- Te reconectas al WiFi

**Verificar IP actual:**
```powershell
ipconfig
```
Busca "Dirección IPv4" en tu adaptador de red WiFi/Ethernet

**Actualizar URL:**
Si tu IP cambió a `192.168.0.X`, usa:
```
http://192.168.0.X:5000/formulario
```

### Problema 3: Solo funciona en mi computadora

**Verificar que el servidor esté en modo red:**
1. Mira la consola donde corre Python
2. Debe decir: `Running on http://0.0.0.0:5000`
3. Si dice `http://127.0.0.1:5000` → reinicia con el nuevo script

---

## 🌍 OPCIONES PARA ACCESO DESDE INTERNET

Si los investigadores NO están en la red local de UPIIZ:

### Opción 1: Ngrok (Temporal - Gratis) 🚀

1. **Instalar ngrok:**
   - Descarga: https://ngrok.com/download
   - Descomprime en tu carpeta

2. **Iniciar túnel:**
   ```bash
   ngrok http 5000
   ```

3. **Compartir URL pública:**
   - Ngrok te da una URL como: `https://abc123.ngrok.io`
   - Comparte: `https://abc123.ngrok.io/formulario`
   - ⚠️ La URL cambia cada vez que reinicias ngrok

### Opción 2: Servidor en Línea (Permanente)

**PythonAnywhere (Gratis):**
1. Crear cuenta: https://www.pythonanywhere.com
2. Subir archivos del proyecto
3. Configurar Web App con Flask
4. Obtienes URL permanente: `https://tuusuario.pythonanywhere.com/formulario`

**Heroku (Gratis/Pago):**
1. Similar a PythonAnywhere
2. Más control y opciones

---

## 📊 MONITOREAR FORMULARIOS RECIBIDOS

### Panel de Administración:

**En tu PC:**
```
http://localhost:5000/panel-formularios
```

**Desde otra PC en la red:**
```
http://192.168.0.4:5000/panel-formularios
```

### Estadísticas en Tiempo Real:
- Total de formularios
- Investigadores con SNII
- Investigadores con EDI
- Investigadores con proyectos

---

## 🔐 SEGURIDAD Y PRIVACIDAD

### Datos Almacenados:

**Ubicación:**
```
DeptoInv/formularios/
├── investigador_12345_20251012_081229.json
└── constancias_snii/
    └── snii_12345_20251012_081229.pdf
```

**Respaldo:**
1. Copia la carpeta `formularios/` completa
2. Guárdala en ubicación segura
3. Incluye JSONs y PDFs

### Acceso:
- **Red Local:** Solo personas en red UPIIZ
- **Internet (ngrok):** Cualquiera con la URL
- **Recomendación:** Usa red local para mayor seguridad

---

## 📅 FLUJO DE TRABAJO RECOMENDADO

### Semana 1: Recolección
1. ✅ Iniciar servidor: `iniciar_sistema_red.bat`
2. ✅ Compartir URL por email/WhatsApp
3. ✅ Monitorear en panel: `http://192.168.0.4:5000/panel-formularios`
4. ✅ Recordatorios a investigadores que faltan

### Semana 2: Cierre
1. ✅ Último recordatorio
2. ✅ Exportar a Excel: Botón en panel
3. ✅ Respaldar carpeta `formularios/`
4. ✅ Detener servidor (Ctrl+C)

### Análisis:
1. ✅ Abrir Excel generado
2. ✅ Filtrar y analizar datos
3. ✅ Generar reportes institucionales

---

## 📞 SOPORTE TÉCNICO

### Tu Información:
- **IP Local:** 192.168.0.4
- **Puerto:** 5000
- **URL Formulario:** http://192.168.0.4:5000/formulario
- **URL Panel:** http://192.168.0.4:5000/panel-formularios

### Comandos Útiles:

```powershell
# Ver tu IP actual
ipconfig

# Verificar que el servidor esté corriendo
netstat -an | findstr :5000

# Agregar regla de firewall
netsh advfirewall firewall add rule name="Flask UPIIZ" dir=in action=allow protocol=TCP localport=5000

# Ver formularios recibidos
dir formularios\*.json
```

---

## ✨ RESUMEN RÁPIDO

### Para Iniciar:
1. `iniciar_sistema_red.bat`
2. Compartir: `http://192.168.0.4:5000/formulario`
3. Monitorear: `http://192.168.0.4:5000/panel-formularios`

### Para Investigadores:
- Solo necesitan el link
- Funciona en PC, tablet, celular
- No necesitan instalar nada
- Datos se guardan automáticamente

### Para Ti (Administrador):
- Panel web para ver todos los formularios
- Botón para exportar a Excel
- Búsqueda rápida de investigadores
- Estadísticas en tiempo real

---

## 🎓 UPIIZ - Instituto Politécnico Nacional

**Departamento de Investigación**  
M. en C. Rafael Reveles Martínez  
📧 investigacion_UPIIZ@ipn.mx  
☎️ Ext. 83530

🌐 [www.zacatecas.ipn.mx](https://www.zacatecas.ipn.mx)

**La Técnica al Servicio de la Patria**

© 2025

