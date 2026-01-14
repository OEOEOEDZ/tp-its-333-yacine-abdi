Health Service
===============

Service to store simple health parameters per person.

Endpoints (all require `Authorization: Bearer <token>`):
- GET /health/<person_id>
- POST /health/<person_id>  (JSON body)
- PUT /health/<person_id>   (JSON body)
- DELETE /health/<person_id>

Environment variables
- SECRET_KEY (shared with person-service to validate tokens)
- PERSON_SERVICE_URL (default http://person-service:5001)
- DATA_FILE (default data.json)

Init data file
- docker run --rm -v $(pwd):/app health-service flask init-data

Run with docker-compose (later)
