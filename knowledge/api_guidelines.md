# API Guidelines

## Synchronous REST

Synchronous REST APIs should be preferred when the caller requires
an immediate response.

REST is appropriate for request-response interactions where the
caller needs the result before continuing.

## Asynchronous Communication

Asynchronous messaging should be considered when the caller does not
need an immediate response or when downstream processing can happen
independently.

## API Design

APIs should use meaningful resource-oriented URLs.

API contracts should be versioned when backward-incompatible changes
are introduced.
