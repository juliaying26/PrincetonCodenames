# TRA 301 Final Project

## Julia Ying & Nora Graves

### Setup:

Backend:

- `cd backend`.
- Run `pip install -r requirements.txt`.
- Run `python game.py` to start the backend (Flask) server.

Frontend:

- Open a new terminal.
- `cd frontend`.
- Run `npm install` (make sure you are in `frontend`). This will install a `node_modules` folder inside `frontend` which is not and should not be pushed to repo.
- Run `npm run dev` to start the frontend (Vite) server.

Navigate to `localhost:5173` to see the webpage.


### Other Possible Setup
Create conda environment: 

- `conda create -n tra301 python=3.12 -y`
- `conda activate tra301`

Install NodeJS:

- `conda config --add channels conda-forge`
- `conda install nodejs`

Backend: 

- `cd backend`
- `pip install psycopg2-binary`
- Run `pip install -r requirements2.txt`.
- Run `python game.py` to start the backend (Flask) server.

Frontend:

- Open a new terminal.
- `cd frontend`.
- `conda activate tra301`
- Run `npm install` (make sure you are in `frontend`). This will install a `node_modules` folder inside `frontend` which is not and should not be pushed to repo.
- Run `npm run dev` to start the frontend (Vite) server.

Navigate to `localhost:5173` to see the webpage.