# FAQ Suggestion API

API para sugerir respuestas FAQ usando similitud de texto.

## ¿Por qué difflib?

Decidí usar `difflib.SequenceMatcher` en lugar de modelos de NLP más pesados por tres razones:

1. **Sin dependencias de ML/NLP** - Solo usa stdlib de Python (difflib)
2. **Suficiente para datasets pequeños** - Funciona bien con <1000 FAQs
3. **Deploy instantáneo** - No hay que descargar modelos de 500MB

Si esto escalara a 10k+ FAQs, lo lógico sería migrar a embeddings semánticos (sentence-transformers), pero para esta prueba técnica prefería mantenerlo simple.

## 🚀 Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

#### Paso 1: Clonar y Construir
```bash
# Clonar el repositorio
git clone https://github.com/FernandoOro/faq-suggestion-simple-system.git
cd faq-suggestion-simple-system

# Construir y levantar el contenedor
docker-compose up --build
```

**Salida esperada:**
```
Creating faq-suggestion-api ... done
Attaching to faq-suggestion-api
api_1  | INFO:     Started server process [1]
api_1  | INFO:     Application startup complete.
api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

La API estará disponible en **http://localhost:8000**

---

#### Paso 2: Verificar que Funciona

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "knowledge_entries": 15,
  "history_entries": 0
}
```

**Documentación Interactiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### Opción 2: Sin Docker (Local)
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📡 Probar los Endpoints

### 1️⃣ **Documentación Interactiva (Más Fácil)**

Abre http://localhost:8000/docs en tu navegador.

Aquí puedes:
- Ver todos los endpoints con ejemplos
- Probar cada uno con el botón "Try it out"
- Ver respuestas en tiempo real
- Descargar el schema OpenAPI

---

### 2️⃣ **Ejemplos con cURL**

#### A. Obtener Sugerencia
```bash
curl -X POST http://localhost:8000/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": "como reseteo mi contraseña"}'
```

**Respuesta:**
```json
{
  "query": "como reseteo mi contraseña",
  "suggestion": "Para resetear tu contraseña, ve a la página de inicio de sesión y haz clic en '¿Olvidaste tu contraseña?'. Ingresa tu correo electrónico y recibirás un enlace para crear una nueva contraseña.",
  "confidence": 0.926
}
```

---

#### B. Ver Historial de Consultas
```bash
curl http://localhost:8000/api/v1/history
```

**Respuesta:**
```json
{
  "total": 1,
  "queries": [
    {
      "timestamp": "2025-12-23T15:30:00.123456",
      "query": "como reseteo mi contraseña",
      "suggestion": "Para resetear tu contraseña...",
      "confidence": 0.926
    }
  ]
}
```

**Con límite:**
```bash
curl "http://localhost:8000/api/v1/history?limit=5"
```

---

#### C. Agregar Nueva FAQ
```bash
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cómo cambio mi foto de perfil?",
    "answer": "Ve a Configuración > Perfil > Cambiar foto de perfil."
  }'
```

**Respuesta:**
```json
{
  "message": "Knowledge entry added successfully",
  "total_entries": 16
}
```

Ahora puedes buscar la nueva pregunta:
```bash
curl -X POST http://localhost:8000/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": "como cambio mi foto"}'
```

---

#### D. Casos de Error

**Query vacía:**
```bash
curl -X POST http://localhost:8000/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": ""}'
```
Retorna `422 Unprocessable Entity`

**Pregunta duplicada:**
```bash
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cómo reseteo mi contraseña?",
    "answer": "Otra respuesta"
  }'
```
Retorna `409 Conflict`

**Sin coincidencias:**
```bash
curl -X POST http://localhost:8000/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": "xyz random text 12345"}'
```
Retorna `404 Not Found`

---

### 3️⃣ **Script de Prueba Automatizado**

Guarda esto como `test_api.sh`:
```bash
#!/bin/bash

echo "🧪 Testing FAQ Suggestion API"
echo "================================"

API_URL="http://localhost:8000"

echo -e "\n1️⃣ Health Check..."
curl -s $API_URL/health | python3 -m json.tool

echo -e "\n2️⃣ Getting Suggestion..."
curl -s -X POST $API_URL/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": "como reseteo mi contraseña"}' | python3 -m json.tool

echo -e "\n3️⃣ Checking History..."
curl -s $API_URL/api/v1/history | python3 -m json.tool

echo -e "\n4️⃣ Adding New Knowledge..."
curl -s -X POST $API_URL/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Pregunta de prueba?", "answer": "Respuesta de prueba"}' | python3 -m json.tool

echo -e "\n5️⃣ Testing New Knowledge..."
curl -s -X POST $API_URL/api/v1/suggest \
  -H "Content-Type: application/json" \
  -d '{"query": "pregunta de prueba"}' | python3 -m json.tool

echo -e "\n✅ All tests completed!"
```

Ejecuta:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 🧪 Ejecutar Tests

### Con Docker
```bash
# Entrar al contenedor en ejecución
docker-compose exec api bash

# Dentro del contenedor, ejecutar tests
pytest --cov=app --cov-report=term-missing

# Salir del contenedor
exit
```

### Sin Docker
```bash
pytest --cov=app --cov-report=term-missing
```

**Salida esperada:**
```
======================== test session starts =========================
collected 28 items

tests/test_suggestions.py .........                            [ 32%]
tests/test_history.py ........                                 [ 60%]
tests/test_knowledge.py ...........                            [100%]

---------- coverage: platform linux, python 3.11.x -----------
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
app/__init__.py                           1      0   100%
app/config.py                            15      0   100%
app/dependencies.py                      12      0   100%
app/main.py                              35      2    94%   15-16
app/models/__init__.py                    8      0   100%
app/models/schemas.py                    24      0   100%
app/routers/history.py                   15      0   100%
app/routers/knowledge.py                 18      1    94%   25
app/routers/suggestions.py               23      1    96%   28
app/services/history_service.py          20      1    95%   45
app/services/knowledge_base.py           21      0   100%
app/services/similarity_service.py       18      1    94%   35
-------------------------------------------------------------------
TOTAL                                   210     6    97%

======================== 28 passed in 0.38s ===========================
```

### Tests Específicos
```bash
# Solo tests de sugerencias
pytest tests/test_suggestions.py -v

# Solo un test específico
pytest tests/test_suggestions.py::TestSuggestEndpoint::test_suggest_exact_match -v

# Con output detallado
pytest -v --tb=short
```

---

## 📊 Endpoints Disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check con métricas |
| GET | `/docs` | Documentación interactiva (Swagger UI) |
| GET | `/redoc` | Documentación alternativa (ReDoc) |
| POST | `/api/v1/suggest` | Obtener sugerencia basada en query |
| GET | `/api/v1/history` | Ver historial de consultas |
| POST | `/api/v1/knowledge` | Agregar nueva FAQ dinámicamente |

---

## 🐳 Comandos Docker Útiles
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver solo errores
docker-compose logs | grep ERROR

# Ver últimas 50 líneas
docker-compose logs --tail=50

# Ver estado de contenedores
docker-compose ps

# Reiniciar el servicio
docker-compose restart

# Ver uso de recursos
docker stats faq-suggestion-api

# Reconstruir sin cache
docker-compose build --no-cache

# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Ejecutar comando puntual sin entrar al contenedor
docker-compose exec api pytest tests/test_suggestions.py
```

---

## 🔧 Solución de Problemas

### Puerto 8000 ya en uso
```bash
# Ver qué proceso usa el puerto
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 externamente
```

### Cambios en el código no se reflejan
```bash
# Reconstruir la imagen
docker-compose up --build
```

### Error al cargar initial_knowledge.json
```bash
# Verificar que el archivo existe
docker-compose exec api ls -la data/

# Ver contenido del archivo
docker-compose exec api cat data/initial_knowledge.json
```

### Tests fallan
```bash
# Ver logs detallados
docker-compose exec api pytest -v --tb=short

# Limpiar caché de pytest
docker-compose exec api pytest --cache-clear
```

### API no responde
```bash
# Ver logs del contenedor
docker-compose logs api

# Verificar que el contenedor está corriendo
docker-compose ps

# Reiniciar
docker-compose restart
```

---

## 📋 Decisiones Técnicas

- **Sin dependencias de ML/NLP** - Solo usa stdlib de Python (difflib) para búsqueda de similitud
- **Singleton pattern** - Servicios en memoria usando `@lru_cache()` (FastAPI no usa threading)
- **Sin persistencia** - Los datos se pierden al reiniciar (esto es un demo; en prod usaría Postgres)
- **Threshold 0.6** - Umbral de similitud ajustable en `dependencies.py`
- **CORS habilitado** - Por si quiero hacer un frontend más adelante
- **Routers síncronos** - Las funciones usan `def` (no `async`) porque `difflib` es CPU-bound. FastAPI las ejecuta en threadpool automáticamente, evitando bloquear el event loop
- **Lifespan Manager** - Carga `initial_knowledge.json` una sola vez al iniciar la aplicación (no en cada request)
- **Logging estructurado** - Usa el módulo `logging` de Python en lugar de `print()` para debugging en producción

---

## 🚀 Mejoras Futuras

- [ ] Agregar caché de queries frecuentes con Redis
- [ ] Implementar fuzzy matching para typos (python-Levenshtein)
- [ ] Endpoint para analytics (queries más comunes, confianza promedio)
- [ ] Persistencia en base de datos (PostgreSQL)
- [ ] Autenticación JWT para endpoints de administración
- [ ] Rate limiting para prevenir abuso
- [ ] CI/CD con GitHub Actions
- [ ] Migrar a embeddings semánticos si el dataset crece >1000 FAQs

---

## ✅ Checklist de Verificación

Antes de entregar, verifica:

- [ ] `docker-compose up --build` funciona sin errores
- [ ] http://localhost:8000/health retorna status "healthy"
- [ ] http://localhost:8000/docs muestra la documentación
- [ ] POST /api/v1/suggest retorna sugerencias correctas
- [ ] GET /api/v1/history muestra el historial
- [ ] POST /api/v1/knowledge permite agregar FAQs
- [ ] `docker-compose exec api pytest` pasa todos los tests (28/28)
- [ ] Cobertura de tests >= 80% (actualmente 97%)

---

## 📝 Estructura del Proyecto
```
faq-suggestion-simple-system/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + Lifespan + CORS
│   ├── config.py            # Logging + Configuración
│   ├── dependencies.py      # Singleton con @lru_cache
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # 7 Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── knowledge_base.py      # Gestión de FAQs
│   │   ├── similarity_service.py  # difflib logic
│   │   └── history_service.py     # Historial en memoria
│   └── routers/
│       ├── __init__.py
│       ├── suggestions.py   # POST /suggest
│       ├── history.py       # GET /history
│       └── knowledge.py     # POST /knowledge
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures de pytest
│   ├── test_suggestions.py  # 9 tests
│   ├── test_history.py      # 8 tests
│   └── test_knowledge.py    # 11 tests
├── data/
│   └── initial_knowledge.json  # 15 FAQs iniciales
├── Dockerfile               # Imagen optimizada
├── docker-compose.yml       # Orquestación
├── requirements.txt         # Dependencias Python
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🎯 Tecnologías Utilizadas

- **Python 3.11** - Lenguaje de programación
- **FastAPI 0.109** - Framework web moderno y rápido
- **Pydantic 2.5** - Validación de datos
- **difflib** - Búsqueda de similitud (stdlib)
- **pytest 7.4** - Testing framework
- **Docker** - Containerización
- **uvicorn** - ASGI server
