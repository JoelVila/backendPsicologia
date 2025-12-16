# Backend Psicología - Documentación del Proyecto

Este repositorio contiene la API Backend para la aplicación de Psicología. A continuación se detallan los cambios más recientes, la estructura de seguridad y dónde localizar los archivos clave.

## 🚀 Últimos Cambios Aplicados (Diciembre 2025)

### 1. Seguridad con JWT (JSON Web Tokens)
Se ha implementado un sistema de autenticación completo.
- **Antes**: Los endpoints eran públicos o usaban mecanismos inconsistentes.
- **Ahora**:
    - **Público**: Login y Registro (`/auth/login`, `/auth/register`).
    - **Privado**: Todas las rutas de negocio (`/main/...`) requieren un Token Bearer.

### 2. Actualización del Modelo `Psicologo`
Se han añadido nuevos campos para la acreditación profesional.
- **Archivos Modificados**: `app/models/Psicologo.py`, `app/routes/auth.py`
- **Nuevos Campos**:
    - `numero_licencia`: Para el número de colegiado.
    - `institucion`: Universidad o entidad emisora.
    - `documento_acreditacion`: Ruta/URL del documento o foto subida.

### 3. Corrección de Inconsistencias Database-Código
Se arreglaron errores donde el código buscaba campos que no existían en la BD.
- Corrección: `contrasena` -> `contrasenia`
- Corrección: `nombre` -> `nombre_completo` (en Paciente)
- Corrección: Centralización del login/registro en `auth.py`, eliminando duplicados de `main.py`.

---

## 📂 Dónde Localizar cada cosa

### Rutas (Endpoints)
- **Autenticación (Login/Registro)**:
  `app/routes/auth.py`
  *Aquí está la lógica de creación de usuarios y generación de tokens.*

- **Lógica Principal (Citas, Historial, Perfiles)**:
  `app/routes/main.py`
  *Aquí están los endpoints protegidos con `@jwt_required()`.*

### Modelos de Base de Datos
- **Psicólogo**:
  `app/models/Psicologo.py`
  *Contiene los nuevos campos de licencia e institución.*

- **Paciente**:
  `app/models/Paciente.py`

---

## 🛠️ Cómo Probar la API

### 1. Registrar un Usuario (Ejemplo Psicólogo)
**POST** `/auth/register`
```json
{
  "role": "psicologo",
  "email": "psi@test.com",
  "password": "123",
  "numero_licencia": "AB-12345",
  "institucion": "Universidad de Barcelona"
}
```

### 2. Iniciar Sesión
**POST** `/auth/login`
```json
{
  "email": "psi@test.com",
  "password": "123",
  "role": "psicologo"
}
```
*Respuesta:* Recibirás un `access_token`.

### 3. Acceder a Datos
**GET** `/main/psicologos`
*Header:* `Authorization: Bearer <TU_ACCESS_TOKEN>`

---

## 🔮 Próximos Pasos (En Progreso)
- **OCR / Análisis de Documentos**: Se está preparando la integración para leer automáticamente los datos del documento de acreditación usando IA.
