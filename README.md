## Initialize sqlite database
>$ ./scripts/init_db.sh
## Drop sqlite database
Either delete the sqlite file, or run this command
>$ ./scripts/drop_db.sh
## Style python code
>$ ./scripts/autopep8.sh
## Run test
>$ ./scripts/test.sh
## Synchronous between master and slave app
    When insert/update user or resume into the master app's database, the master app will send http requests to the slave app, so that the slave can sync its database with the master's database.
    The slave app is located in branch `slave`, run its on port 4000 with `flask run --port 4000`.
