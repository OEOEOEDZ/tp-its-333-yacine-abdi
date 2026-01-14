Person Service
================

Small Flask microservice that manages persons.

Endpoints
- POST /persons  {"name": "Alice"}  -> 201 {"id": 1, "name": "Alice"}
- GET /persons/<id>  -> 200 or 404
- DELETE /persons/<id> -> 204 or 404
- POST /auth {"username":..., "password":...} -> 200 {"access_token": "..."}

Environment variables
- SECRET_KEY (used to sign JWT)
- AUTH_USER, AUTH_PASSWORD (for token issuance)
- DATABASE_URL (default: sqlite:///database.db)

Initialize DB
- docker run --rm -e SECRET_KEY=... -e AUTH_USER=... -e AUTH_PASSWORD=... -v $(pwd):/app person-service flask create-db

Run with docker-compose (later)
