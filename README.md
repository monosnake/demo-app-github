# demo-app-github

Aplicación de demostración (FastAPI + PostgreSQL) cuyo pipeline de GitHub
Actions consume credenciales desde HashiCorp Vault. Forma parte del sistema
descrito en el repositorio `vault-central-secrets`.

## Pipelines

- **`ci-vault.yml`** (enfoque propuesto): el job se autentica ante Vault con
  el token OIDC que GitHub emite por ejecución (`permissions: id-token: write`),
  sin ningún secreto almacenado en GitHub. Obtiene credenciales dinámicas de
  PostgreSQL (TTL de 5 minutos) para las pruebas de integración, la clave de
  API desde KV v2 para el build, y despliega el contenedor inyectando en
  tiempo de ejecución la credencial estática que Vault rota cada 24 horas.
- **`ci-baseline.yml`** (enfoque tradicional, para la comparativa): usa
  credenciales de larga vida almacenadas como GitHub Secrets
  (`DB_USER`, `DB_PASSWORD`, `EXTERNAL_API_KEY`).

Ambos corren en el runner self-hosted conectado a la red `secrets-net`,
por lo que Vault nunca se expone a internet.

## Desarrollo local

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q          # la prueba de integración se omite sin credenciales
uvicorn app.main:app --reload
```

La aplicación lee su configuración exclusivamente del entorno:
`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
