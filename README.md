# FAQ Suggestion API

API para sugerir respuestas FAQ usando similitud de texto.

## ¿Por qué difflib?

Decidí usar `difflib.SequenceMatcher` en lugar de modelos de NLP más pesados por tres razones:

1. **Sin dependencias de ML/NLP** - Solo usa stdlib de Python (difflib)
2. **Suficiente para datasets pequeños** - Funciona bien con <1000 FAQs
3. **Deploy instantáneo** - No hay que descargar modelos de 500MB

Si esto escalara a 10k+ FAQs, lo lógico sería migrar a embeddings semánticos (sentence-transformers), pero para esta prueba técnica prefería mantenerlo simple.

## Setup Rápido
```bash
# Con Docker
docker-compose up --build

# Sin Docker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

- **POST /api/v1/suggest** - Buscar respuesta similar
- **GET /api/v1/history** - Ver historial de consultas
- **POST /api/v1/knowledge** - Agregar nueva FAQ
- **GET /health** - Health check

Docs interactiva: http://localhost:8000/docs

## Tests
```bash
pytest --cov=app --cov-report=term-missing
```

## Decisiones Técnicas

- **Singleton pattern** - Servicios en memoria usando `@lru_cache()` (FastAPI no usa threading)
- **Sin persistencia** - Los datos se pierden al reiniciar (esto es un demo; en prod usaría Postgres)
- **Threshold 0.6** - Umbral de similitud ajustable en `dependencies.py`
- **CORS habilitado** - Por si quiero hacer un frontend más adelante
- **Routers síncronos** - Las funciones usan `def` (no `async`) porque `difflib` es CPU-bound. FastAPI las ejecuta en threadpool automáticamente, evitando bloquear el event loop.

## Mejoras Futuras

- [ ] Agregar caché de queries frecuentes con Redis
- [ ] Implementar fuzzy matching para typos
- [ ] Endpoint para analytics (queries más comunes)
