# TRA 301 Final Project

## Julia Ying & Nora Graves

### Demo:

Navigate to https://princetoncodenames.onrender.com/. It may take up to a minute to load if no one has been on the website in a while. Note that only one player may use the website at a time (if more than one player, all changes will show up on the website).

### Setup:

Backend:

- Open a terminal for the backend.
- `cd backend`.
- Run `pip install -r requirements.txt`.
- Run `python game.py` to start the backend (Flask) server.

Frontend:

- Keep the backend terminal running and open a new terminal for the frontend.
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
