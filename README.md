FALSE GODS: Web Strategy Game

This is a work-in-progress strategy game inspired by the history of ancient Mesopotamia. Imagine a Heroes of M&M style world map, but set between the great rivers of the cradle of civilization—where rituals and sacrifices weigh as heavily as armies and gold.

## Features

- FastAPI backend
- React + Vite frontend (interactive UI)
- SQLite with SQLAlchemy ORM

## Project Structure

```
root/
│
├── app/            # FastAPI backend app (APIs, models, repositories)
├── frontend/       # React + Vite app
├── README.md
├── requirements.txt
└── package.json
```

## Installation

### 1. Backend (FastAPI)

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd app
uvicorn api.api:app --reload
```

Backend runs at: [http://localhost:8000](http://localhost:8000)

### 2. Frontend (React + Vite)

```sh
cd frontend
npm install
npm run dev
```

Frontend runs at: [http://localhost:5173](http://localhost:5173)

## Development Notes

- To run the full app, start backend + frontend in parallel.
- API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)
<!-- - See `app/README.md` for DB details.
- See `frontend/README.md` for React commands. -->

## License

This project is licensed under the [MIT License](LICENSE).