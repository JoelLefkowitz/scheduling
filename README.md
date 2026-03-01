# Scheduling

![Review](https://img.shields.io/github/actions/workflow/status/JoelLefkowitz/scheduling/review.yaml)

Scheduling ingestion layer.

- [Usage](#usage)
- [Examples](#examples)
- [Tooling](#tooling)

## Usage

### Installing

```sh
poetry install --with all
```

This installs all the project dependencies and the development tooling.

### Running

To start the application, set these environment variables:

| Variable                      | Value                         |
| ----------------------------- | ----------------------------- |
| `DJANGO_SETTINGS_MODULE`      | `"scheduling.settings.local"` |
| `DJANGO_SECRET_KEY`           | Generate a random key         |
| `DJANGO_FIELD_ENCRYPTION_KEY` | Generate a random key         |

Start the database container:

```sh
docker compose up database
```

Start the development server:

```sh
python src/manage.py runserver
```

This will connect your server with the database container:

<div align='center'>
    <img src="./docs/images/environments-localhost.png" width="400">
</div>

#### Containerisation

To run as the api service as a container set the postgres host to the service name:

| Variable        | Value                   |
| --------------- | ----------------------- |
| `POSTGRES_HOST` | `"scheduling-database"` |

```sh
docker compose up --build
```

This will launch and connect an api service container with the database container:

<div align='center'>
    <img src="./docs/images/environments-container.png" width="400">
</div>

#### Production

To run in production, set these environment variables:

| Variable                 | Value                        |
| ------------------------ | ---------------------------- |
| `DJANGO_SETTINGS_MODULE` | `"scheduling.settings.prod"` |
| `DJANGO_HOST_DOMAIN`     | Deployment domain            |
| `POSTGRES_DB`            | Database name                |
| `POSTGRES_USER`          | Database user                |
| `POSTGRES_PASSWORD`      | Database password            |

### Endpoints

The application exposes the following endpoints:

| Endpoint   | Purpose                         |
| ---------- | ------------------------------- |
| `/ingest/` | HL7 procedure ingestion service |
| `/admin/*` | Django admin interface          |
| `/docs/`   | Swagger UI (OpenAPI)            |

## Examples

> Unit tests for these requests/responses are in `tests/*`.

### Procedure creation

Given a valid HL7 procedure payload a procedure and patient instance are created.

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

### Parsing errors

If the HL7 payload cannot be parsed, a structured error message is returned.

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

### Validation errors

If the HL7 payload contains invalid field data, a structured error message is returned.

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
