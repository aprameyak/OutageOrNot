# OutageOrNot

OutageOrNot gives a rough read on whether the weather could knock out power in a U.S. state. It pulls the current National Weather Service forecast and active alerts for the state and asks GPT-3.5 Turbo to label the outage risk as very unlikely, unlikely, likely, or very likely.

It was built for the Google Solution Challenge 2025. The risk label is an LLM's judgment from a prompt, not a trained or validated prediction model.

## Usage

Enter a two-letter state code in the web app, or call the API directly:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"state": "TX"}'
```

A successful response has this shape, where `data` is the model's short text answer:

```json
{ "success": true, "data": "<risk label>" }
```

Errors return `{"error": "...", "message": "..."}` with status 400 (bad or missing state) or 500.

## Features

- Accepts any of the 50 state codes and maps it to a fixed point near the state's center (`findLocation` in `model.py`).
- Fetches the NWS 7-day forecast, hourly forecast, and active alerts for that point from `api.weather.gov`.
- Sends temperature, wind speed and direction, precipitation probability, and alert details to `gpt-3.5-turbo` with a prompt that asks for a one-or-two-word risk label.
- Next.js page with a state input that shows the result or the API error.
- `/health` endpoint for uptime checks.

## Tech stack

- Backend: Python, Flask, flask-cors, requests, OpenAI Python SDK
- Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS, axios
- Data: National Weather Service API (no key required)

## Getting started

Prerequisites: Python 3.11, Node.js 20, and an OpenAI API key.

Environment variables:

- Backend (`.env` in the repo root, loaded with python-dotenv): `OPENAI_API_KEY`, optional `PORT` (default 5000) and `FLASK_DEBUG` (default `True`)
- Frontend: optional `NEXT_PUBLIC_API_URL` (default `http://localhost:5000`)

Backend:

```bash
pip install -r requirements.txt
pip install "openai<1"
python api.py
```

The second install is needed because `model.py` calls `openai.ChatCompletion.create`, which was removed in version 1.0 of the OpenAI SDK, while `requirements.txt` asks for `openai>=1.59.0`. With a 1.x SDK installed, `/predict` returns a 500 error.

Frontend, in a second terminal:

```bash
cd frontend
npm install
npm run dev      # http://localhost:3000
```

There are no automated tests. CI (`.github/workflows/ci.yml`) only checks that the backend and frontend dependencies install.

## How it works

- `api.py`: Flask app with `GET /health` and `POST /predict`. It validates the state code, calls `getWeatherData`, and logs to `app.log`.
- `model.py`: `findLocation` maps the state to coordinates, `get_relevant_nws_data` calls the NWS `points`, `forecast`, `forecast/hourly`, and `alerts/active` endpoints, and `getWeatherData` builds the prompt and returns the model's reply.
- `frontend/app/page.tsx`: the single page UI. `frontend/app/api/client.ts` wraps the `/predict` and `/health` calls.

Because each state is reduced to one point, the result reflects the weather at that point, not across the whole state.

## Contributing

Issues and pull requests are welcome. Before opening a PR, run the backend and frontend locally and check a `/predict` request end to end, and run `npm run build` in `frontend/`.

## License

MIT, see [LICENSE](LICENSE).
