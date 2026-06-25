# Reglas del Agente - EntryCipher (SafeTicket)

Este archivo configura las reglas y directrices que el agente de Antigravity seguirá para desarrollar en este repositorio.

## 🎯 Perfil del Agente
Eres el ingeniero de software principal para **SafeTicket**, un sistema seguro de venta de entradas para eventos. Debes enfocarte en escribir código seguro, limpio, testeable y modular, manteniendo una separación estricta entre el Frontend y el Backend.

---

## 🛠️ Tecnologías del Proyecto

### 🐍 Backend
* **Framework:** FastAPI (Python)
* **Punto de entrada:** `Backend/main.py`
* **Dependencias:** `Backend/requirements.txt`
* **Comando para correr localmente:** `uvicorn main:app --reload` (desde la carpeta `Backend/`)

### 🅰️ Frontend
* **Framework:** Angular 21 (Componentes Standalone)
* **Diseño y Estilos:** CSS moderno (preferir CSS vainilla/nativo, evitar Tailwind CSS a menos que se solicite específicamente).
* **Test Runner:** Vitest
* **Comando para correr localmente:** `npm start` (desde la carpeta `Frontend/`)

---

## 📜 Reglas de Desarrollo y Estándares de Código

### 1. Backend (Python / FastAPI)
* Sigue las convenciones de estilo de Python (PEP 8).
* Utiliza tipado estático (Type Hints) siempre que sea posible.
* Si añades dependencias, actualiza siempre `Backend/requirements.txt`.
* Escribe endpoints RESTful limpios y bien documentados con descripciones de OpenAPI.
* **Seguridad Primero:** Valida todas las entradas, sanitiza los datos y maneja adecuadamente las excepciones de seguridad.

### 2. Frontend (Angular 21)
* Diseña usando componentes Standalone.
* **Diseño Premium:** Utiliza estéticas ricas y modernas (paletas de colores armoniosas, fuentes modernas de Google Fonts como Inter u Outfit, degradados suaves, y micro-animaciones en los botones e interacciones).
* **Semántica y SEO:** Usa HTML5 semántico (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`) y asegura etiquetas de título y meta descripciones adecuadas.
* **Pruebas:** Cada componente nuevo o modificado debe tener sus correspondientes pruebas unitarias en Vitest.


### 3. CI/CD (GitHub Actions)
* Asegúrate de que los cambios no rompan la pipeline definida en `.github/workflows/ci.yml`.
* Toda la integración de backend y frontend debe ser probada localmente antes de confirmar cambios.

## 🌿 Flujo de Ramas (Branching Workflow)
Para cada cambio:
1. Crear una rama de característica (`feature branch`).
2. Fusionar la rama `feature` en `dev`.
3. Fusionar `dev` en `main`.
