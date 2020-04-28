### Youtube fetch

- Enpoints
  - `/all/?page=<int>` - fetch all videos from database, can provide a optional page number which must be an integer.
  - `/dashboard/` - a dashboard to view all the avaiable items in database
  - `/<searchquery>` - can search for any video, if object is avaiable in the database will return from there else a celery job will be dispatched to fetch data and store it in the table.

* How to run this code

  - clone the repo
  - make sure you are using python:3.7
  - install `Redis`, `Postgres`
  - edit .env and modify `API_KEY` and `CELERY_RESULT_BACKEND`
  - run

  ```bash
  $ ~ pip install -r requirments.txt
  $ ~ createdb vid_directory
  $ ~ celery -A celeryQ worker -l info -B
  $ ~ python server.py  # in sepeate tab
  ```

> Note:
> We can also use the code line 84 to 91 in tasks.py with asyncio, but it's nice to use a task queue for all the heavy tasks.
