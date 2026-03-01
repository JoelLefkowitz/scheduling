# Scheduling

![Review](https://img.shields.io/github/actions/workflow/statuContents:
s/JoelLefkowitz/scheduling/review.yaml)

Scheduling ingestion layer.

- [Usage](#usage)
- [Tooling](#tooling)

## Usage

### Installing

```sh
poetry install --with all
```

### Running

Services are containerised and PostgreSQL is used across all environments for consistency and reliability.

#### Local

To run locally, set these environment variables:

- `DJANGO_SETTINGS_MODULE`: `"scheduling.settings.local"`
- `DJANGO_SECRET_KEY`: (generate a random key)
- `DJANGO_FIELD_ENCRYPTION_KEY`: (generate a random key)

##### Connect

![Environments localhost](./docs/images/environments-localhost.png)

Start the database container:

```sh
docker compose up database
```

Start the development server:

```sh
python src/manage.py runserver
```

##### Container

![Environments container](./docs/images/environments-container.png)

When running from inside a container, also set:

- `POSTGRES_HOST`: `"scheduling-database"`

Run both the API and database containers:

```sh
docker compose up --build
```

#### Production

To run in production, set these environment variables:

- `DJANGO_SETTINGS_MODULE`: `"scheduling.settings.prod"`
- `DJANGO_HOST_DOMAIN`: (your domain)
- `POSTGRES_DB`: (database name)
- `POSTGRES_USER`: (database user)
- `POSTGRES_PASSWORD`: (database password)

### Endpoints

| Endpoint        | Purpose                         |
| --------------- | ------------------------------- |
| `POST /ingest/` | HL7 procedure ingestion service |
| `GET /docs/`    | OpenAPI - Swagger UI            |
| `GET /admin/`   | Admin interface                 |

#### Example Responses

All responses are tested in `tests/`. You can test these manually via `/docs/`

##### Success

Request:

```txt
MSH|^~\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S
SCH|A1001|PROC123|20250102|093000|120000
PID|123456|DOE^JOHN
```

Response:

```json
{
  "id": 1,
  "schedule_id": "A1001",
  "procedure_code": "PROC123",
  "procedure_date": "2025-01-02",
  "start_time": "09:30:00",
  "end_time": "12:00:00",
  "patient": {
    "id": 1,
    "patient_id": "123456",
    "first_name": "JOHN",
    "last_name": "DOE"
  }
}
```

##### Parsing errors

Request:

```txt
MSH|^~\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S
SCH|A1001|PROC123|20250102|093000|120000
```

Response:

```json
{
  "type": "client_error",
  "errors": [
    {
      "code": "parse_error",
      "detail": "Expected 3 PID fields",
      "attr": null
    }
  ]
}
```

##### Validation errors

Request:

```txt
MSH|^~\&|EMR|HOSPITAL1|VIDEO_SYS|OUR_PLATFORM|202501011030||SIU^S
SCH|A1001|PROC123|20250102|093000|999999
PID|123456|DOE^JOHN
```

Response:

```json
{
  "type": "validation_error",
  "errors": [
    {
      "code": "invalid",
      "detail": "Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].",
      "attr": "end_time"
    }
  ]
}
```

### Tooling

`just` is used to aggregate tooling scripts into groups:

#### Linters

```sh
just lint
```

#### Formatters

```sh
just format
```

#### Tests

```sh
just test
```
