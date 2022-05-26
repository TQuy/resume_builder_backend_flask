## Get started with [Flask][flask] and its extensions
1. Basic setup of Flask project with its extensions ([Flask-SQLAlchemy][flask-sqlalchemy], [Flask-Migrate][flask-migrate], [Flask-CORS][flask-cors], [flask-restx][flask-restx], ...), following [Application Factories][application-factories] structure, can be seen in this sample project. Start reading from `flaskr/__init__.py` file.
2. The package [flask-restplus][flask-restplus] is no longer maintained (I tried integrating the latest version of the package with this project but failed). You can work around by either downgrading the package version, or use [flask-restx][flask-restx] like I did.
3. Some functions which interact with databases (for example) need application context. View `flaskr/test.ipynb` to see how to use application context in your flask shell (use vscode's jupyter notebook to view).
4. [Flask][flask] and its extensions were released 6 years after [Django][django] but have older python coding style, and their documentations (whether by code or by articles) are poor compared to [Django][django]. However, they are more flexible. I don't feel being tied to OOP when using [Flask][flask]. 

## Database Migration
1. In case of **creating/altering** sqlalchemy model, use command `flask db revision` to create migration file, then edit it. I tried using `flask db migrate` but the auto-generated migration file has no information related to the newly created/modified model.
5. Use `existing_*` parameters for fields you don't intend to modify, when writing migration file.
2. Use `flask db upgrade` and `flask db downgrade` to **upgrade/downgrade** migration version.
3. To view the current migration version, use `flask db current` or see `alembic_version` table.
3. Use `flask db upgrade <current_version>:<next_version> --sql` to see the SQL commands needed for the migration.
4. In case you screw up by `dropping table` manually, change the migration version manually in `alembic_version` table.

## Start the application
```
$ export FLASK_ENV=development
$ export FLASK_APP=flaskr
$ flask run --port 5000
```

## Initialize sqlite database
>$ ./scripts/init_db.sh
## Drop sqlite database
Either delete the sqlite file, or run this command
>$ ./scripts/drop_db.sh
## Style python code
>$ ./scripts/autopep8.sh
## Run test
>$ ./scripts/test.sh

## API Documents
Utilizing [flask-restx][flask-restx] or [flask-restplus][flask-restplus] to document the APIs. The APIs documents of this project is located in `localhost:5000/api/`.

## Synchronous connection between master and slave app
When insert/update user or resume into the master app's database, the master app will send http requests to the slave app, so that the slave can sync its database with the master's.  
The slave app is located in branch `slave`, run its on port 4000 with `flask run --port 4000` (you may need to merge master branch into slave branch to get the latest update).

## Asynchronous connection between master and slave app
1. When insert/update user or resume into the master app's database, the master app will send message to the message broker (`Apache Kafka`).  
2. Upon receiving messages sent by the master app (`producer`), the message broker send message to `consumer` `flask` app.  
3. The consumer then send `http` request to the `slave` app
4. The `slave` app can update its database following the `master`, by using the information sent from `consumer`.  
   
The `master` app is located in branch `async_master` (again, merge master branch into it to get the latest update).

[flask]: https://flask.palletsprojects.com/en/2.1.x/
[flask-sqlalchemy]: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
[flask-migrate]: https://flask-migrate.readthedocs.io/en/latest/
[flask-cors]: https://flask-cors.readthedocs.io/en/latest/
[application-factories]: https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/#application-factories
[sample-flask-project]: https://git.teko.vn/quy.nt/sqlalchemy-tutorial/-/blob/master/flaskr/__init__.py
[flask-restx]: https://flask-restx.readthedocs.io/en/latest/  
[flask-restplus]: https://flask-restplus.readthedocs.io/en/stable/  
[django]: https://www.djangoproject.com/

## Working with FMS project
1. After setting up **FMS** project following [FMS Getting Started](https://confluence.teko.vn/display/AS/FMS+Getting+started) (some packages in `requirements.txt` needs to be removed). You can see list of API and their information by run the command `flask run`, then follow the link `localhost:5000/api/` 