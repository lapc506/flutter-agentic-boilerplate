# API Gateway & Rate Limiting Scripts

Scripts ejecutables para implementación de API Gateway con rate limiting.

## 📁 Archivos

- **`kong_custom_rate_limiting.lua`** - Plugin personalizado de Kong para rate limiting con Redis
- **`rate_limiting_strategies.py`** - Implementación de algoritmos de rate limiting (Fixed Window, Token Bucket, Sliding Window)
- **`api_gateway_middleware.py`** - Middleware FastAPI con rate limiting y autenticación
- **`requirements.txt`** - Dependencias Python

## 🚀 Quick Start

### Rate Limiting Strategies (Python)

No requiere instalación para uso básico (usa stdlib):

```bash
# Test fixed window rate limiter
python rate_limiting_strategies.py \
  --strategy fixed \
  --max-requests 10 \
  --window 60 \
  --num-requests 15

# Test token bucket
python rate_limiting_strategies.py \
  --strategy token-bucket \
  --capacity 10 \
  --refill-rate 1.0 \
  --num-requests 15

# Test sliding window
python rate_limiting_strategies.py \
  --strategy sliding \
  --max-requests 10 \
  --window 60 \
  --num-requests 15
```

### API Gateway Middleware

Instalación:

```bash
pip install -r requirements.txt
```

Ejecución:

```bash
# Desarrollo
uvicorn api_gateway_middleware:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn api_gateway_middleware:app --host 0.0.0.0 --port 8000 --workers 4
```

Probar:

```bash
# Sin autenticación (rate limit por IP)
curl http://localhost:8000/api/v1/public

# Con API key
curl -H "Authorization: Bearer valid-api-key-1" http://localhost:8000/api/v1/data
```

### Kong Custom Plugin (Lua)

Instalación en Kong:

```bash
# 1. Crear directorio del plugin
mkdir -p /usr/local/share/lua/5.1/kong/plugins/custom-rate-limiting

# 2. Copiar archivos
cp kong_custom_rate_limiting.lua /usr/local/share/lua/5.1/kong/plugins/custom-rate-limiting/access.lua

# 3. Crear schema.lua (ver comentarios en el archivo)

# 4. Habilitar plugin en kong.yml o vía API
```

## 📖 Documentación Completa

Ver [`../SKILL.md`](../SKILL.md) para documentación completa sobre:
- Configuración de Kong
- Configuración de Nginx
- Estrategias de rate limiting
- Mejores prácticas
