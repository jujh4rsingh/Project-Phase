# Atmo Derma Architecture

Atmo Derma is organized around a feedback loop rather than a weather feed:

`profile + environment + exposure -> indicators -> guidance -> check-in -> personal trend`

## Boundaries

- `api/` owns HTTP transport and response contracts.
- `schemas/` owns validated data contracts shared by APIs and services.
- `services/` owns provider adapters, risk calculations, and adaptive guidance.
- `iot/` owns device-facing concerns and the deterministic simulator.
- `config/` owns explainable risk thresholds and weights.
- `frontend/` renders product workflows without owning environmental calculations.

External providers are accessed through service classes. The UI consumes a unified environment snapshot and never calls Open-Meteo directly.

## Safety boundary

Scores are relative environmental exposure indicators, not clinical or diagnostic measurements. Explanations describe associations and available data; they do not claim causation.
