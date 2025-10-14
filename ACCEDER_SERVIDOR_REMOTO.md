# 🌐 ACCEDER A FORMULARIOS DEL SERVIDOR REMOTO

## 📊 SITUACIÓN ACTUAL

### **Servidor Remoto** (donde están los 11 formularios)
- 📍 Ubicación: `~/DeptoInv`
- 📋 Formularios: **11** (Investigadores UPIIZ)
- 🔧 Estado: Operativo en producción

### **PC Local** (solo 1 formulario de prueba)
- 📍 Ubicación: `D:\IDE_Cursor\DeptoInv`
- 📋 Formularios: **1** (tu registro de prueba)

---

## 🚀 MÉTODO 1: ACCEDER VÍA SSH (RECOMENDADO)

### **Paso 1: Conectarte al Servidor**

```bash
# Abre PowerShell y conéctate al servidor
ssh usuario@tu-servidor.com

# O si usas IP:
ssh usuario@192.168.x.x
```

### **Paso 2: Ir al Directorio del Proyecto**

```bash
cd ~/DeptoInv
```

### **Paso 3: Ver Formularios Sin Servidor (Rápido)**

```bash
# Opción A: Resumen simple
python resumen_formularios.py

# Opción B: Ver lista de archivos
ls -lh formularios/*.json

# Opción C: Contar formularios
ls formularios/*.json | wc -l
```

### **Paso 4: Iniciar el Panel Admin en el Servidor**

```bash
# Iniciar servidor Flask
python app.py
```

Luego desde tu navegador local:
```
http://IP-SERVIDOR:5000/admin-login
```

**Token:** `bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU`

---

## 🔄 MÉTODO 2: SINCRONIZAR FORMULARIOS A TU PC

### **Descargar los 11 formularios a tu PC local:**

```bash
# Desde PowerShell en tu PC:
scp -r usuario@servidor:~/DeptoInv/formularios D:\IDE_Cursor\DeptoInv\

# Esto copiará todos los formularios del servidor a tu PC
```

Después podrás verlos localmente:
```bash
cd D:\IDE_Cursor\DeptoInv
python resumen_formularios.py
```

---

## 📥 MÉTODO 3: EXPORTAR A EXCEL DESDE EL SERVIDOR

### **Opción A: Descargar Excel directamente**

Desde el servidor:
```bash
cd ~/DeptoInv
python scripts/exportar_formularios_excel.py
```

Luego descargar el archivo Excel:
```bash
# Desde tu PC
scp usuario@servidor:~/DeptoInv/Formularios_*.xlsx .
```

### **Opción B: Usar el Panel Web**

1. Conectarte al servidor por SSH con túnel:
```bash
ssh -L 5000:localhost:5000 usuario@servidor
```

2. En el servidor:
```bash
cd ~/DeptoInv
python app.py
```

3. En tu navegador local:
```
http://localhost:5000/admin-login
```

4. Usar el botón "📥 Descargar Excel" del panel

---

## 🎯 MÉTODO 4: COMANDOS RÁPIDOS REMOTOS

### **Ver resumen sin iniciar servidor:**

```bash
# Conectar y ejecutar en un comando
ssh usuario@servidor "cd ~/DeptoInv && python resumen_formularios.py"
```

### **Ver lista de investigadores:**

```bash
ssh usuario@servidor "ls -1 ~/DeptoInv/formularios/*.json | xargs -I {} basename {}"
```

### **Contar formularios:**

```bash
ssh usuario@servidor "ls ~/DeptoInv/formularios/*.json | wc -l"
```

---

## 📊 INFORMACIÓN DE LOS 11 FORMULARIOS REMOTOS

Según tu mensaje anterior, estos son los archivos:

```
investigador_121219_20251013_221245.json
investigador_131140_20251013_143526.json
investigador_131171_20251013_173004.json
investigador_170184_20251013_145852.json
investigador_180159_20251013_151050.json
investigador_180337_20251013_202451.json
investigador_210202_20251013_174915.json
investigador_210208_20251013_203228.json
investigador_210208_20251013_203229.json
investigador_210208_20251013_212315.json
investigador_2901989_20251013_192441.json
```

**Total:** 11 investigadores registrados el 13 de octubre de 2025

---

## 🔑 DATOS DE ACCESO

- **Token Admin:** `bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU`
- **Puerto:** 5000
- **URL Login:** `http://localhost:5000/admin-login` (con túnel SSH)

---

## 💡 RECOMENDACIÓN

**La forma MÁS FÁCIL:**

1. Conectarte por SSH al servidor:
   ```bash
   ssh tu-usuario@tu-servidor
   ```

2. Ejecutar el script de resumen:
   ```bash
   cd ~/DeptoInv
   python resumen_formularios.py
   ```

3. Para análisis completo, iniciar el servidor:
   ```bash
   python app.py
   ```

4. Desde otro terminal en tu PC, crear túnel SSH:
   ```bash
   ssh -L 5000:localhost:5000 tu-usuario@tu-servidor
   ```

5. Abrir navegador en: `http://localhost:5000/admin-login`

---

## 🆘 ¿NO TIENES ACCESO SSH?

Si no puedes conectarte por SSH, necesitarías:

1. **Pedir a alguien con acceso** que:
   - Ejecute el servidor en el servidor remoto
   - Te proporcione la IP pública
   - Abra el puerto 5000 en el firewall

2. **O que te envíe** el Excel exportado:
   ```bash
   python scripts/exportar_formularios_excel.py
   ```

---

## 📞 SIGUIENTE PASO

¿Cuál es tu situación?

- [ ] Tienes acceso SSH al servidor
- [ ] No tienes acceso SSH
- [ ] Prefieres que alguien más exporte los datos
- [ ] Otro: _______________

**Dime cómo prefieres proceder y te ayudo con los comandos específicos.**

