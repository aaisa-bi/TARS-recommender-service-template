# TARS-recommender-service-template
![TARS](src/art/tars.jpg)

Template FastAPI service for event-to-action recommendations, using uv for deps, Hydra configs, and Docker for reproducible runs. The service exposes a `/recommend-action` endpoint that authenticates with an `api-key` header and returns a mock action response.

## Quickstart
1) Set env vars: `cp .env.example .env`
- Vars to set:

```bash
API_KEY_HASH=sha-256-of-your-secret-key
PORT=8000 #or other if 8000 is busy

```
2) Build the container: 
    ```bash
    make build #to update the latest changes on the docker image
    ```
3) Run locally: 
    ```bash
    make run  # to run the image in composer with env and credentials
    ```
    you should see the app healthy and running 🚀✅
     ```bash
    app-1  | INFO:     Started server process [19]
    app-1  | INFO:     Waiting for application startup.
    app-1  | 2025-11-26 12:24:24.253 | INFO     | app.main:display_banner:36 - 
    app-1  | ░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓███████▓▒░ 
    app-1  |    ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    app-1  |    ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    app-1  |    ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░  
    app-1  |    ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
    app-1  |    ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
    app-1  |    ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
    app-1  |                                                      
    app-1  |                                                      
    app-1  | 
    app-1  | INFO:     Application startup complete.
    app-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
    ```

4) Call the API:  
   ```bash
   curl -X POST "http://localhost:${PORT:-8000}/recommend-action" \
     -H "Content-Type: application/json" \
     -H "api-key: <your-api-key>" \
     -d '{"id":"evt-1","event_metadata":{},"user_metadata":{}}'
   ```
5) Explore docs/UI in [http://0.0.0.0:8000/docs#](http://0.0.0.0:8000/docs#). The default api_key is `tars`. (needs to be changed in production)


## 🕵🏼‍♂️  ABOUT TESTING: 
    WE ARE SERIOUS PEOPLE AND WE TEST OUR CODE, WE AIM FOR 100% COVERAGE. SO DON'T BE WEAK AND FUCKING TEST!!

```bash
coverage: platform darwin, python 3.12.7-final-0 
__________________________________________________________

Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
src/app/__init__.py                 0      0   100%
src/app/main.py                    23      0   100%
src/app/model/__init__.py           0      0   100%
src/app/model/model_schema.py      15      0   100%
src/app/model/recommender.py       24      0   100%
src/app/utils/__init__.py           0      0   100%
src/app/utils/art.py                9      0   100%
src/app/utils/auth.py              18      0   100%
src/connections/__init__.py         0      0   100%
src/settings.py                     8      0   100%
-------------------------------------------------------------
TOTAL                              97      0   100%
```


## Development workflow
- The easiest way to develop os to use in docker execution (simpler and enforces docker parity). But if you are a caveman, you can still install the project and deps with uv and run `main.py`.
- Local tools (optional): 
    - install uv locally:
    ```bash
     pip install uv
     uv sync --python 3.12
     ``` 
- Lint/typecheck/tests (PEP8 + typing encouraged): 
    - `make lint`
    - `make typecheck`
    - `make test` (includes coverage report)
- Config defaults live in `src/app/config/default.yaml`; update and rebuild to change action defaults.  
- Credential files live in `credentials/` (git-kept via `.gitkeep` but contents ignored); mount is read-only in compose.  
- Follow `AGENTS.md` for project standards (typing, logging with loguru/structlog, Hydra configs).
