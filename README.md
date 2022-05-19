## Get started with `Flask` and its extensions
1. Basic setup of Flask project with its extensions (`Flask-SQLAlchemy`, `Flask-Migrate`, `Flask-CORS`, `flask-restplus`, ...), following [Application Factories][application-factories] structure, can be seen in my sample project [flask-tutorial][sample-flask-project], in file `flaskr/__init__.py`.
2. The package `flask-restplus` is no longer maintained (I tried integrating the latest version of the package with my sample project  flask-tutorial but failed). You can work around by either downgrading the package version, or just read the document like I do.
3. **SQLAlchemy ORM** seems to be more flexible compare to **Django ORM**, but its documents are such a mess.
4. Some functions which interact with databases (for example) need application context. View `flaskr/test.ipynb` to see how to use application context  in your `flask shell` (use **vscode**'s **jupyter notebook** to view).
## Database Migration
1. In case of **creating/altering** sqlalchemy model, use command `flask db revision` to create migration file, then edit it. I tried using `flask db migrate` but the auto-generated migration file has no information related to the newly created/modified model.
5. Use `existing_*` argument for fields you don't want to modify, when writing migration file.
2. Use `flask db upgrade` and `flask db downgrade` to **upgrade/downgrade** migration version.
3. To view the current migration version, use `flask db current` or see `alembic_version` table.
3. Use `flask db upgrade <current_version>:<next_version> --sql` to **simulate** the migration and see the logs (I tested and this command didn't upgrade the database).
4. In case you screw up by `dropping table` manually, change the migration version manually in `alembic_version` table.
## Working with FMS project
1. After setting up **FMS** project following [FMS Getting Started](https://confluence.teko.vn/display/AS/FMS+Getting+started) (some packages in `requirements.txt` needs to be removed). You can see list of API and their information by start **Flask** `flask run`, then follow the link `localhost:5000/api/` 

[application-factories]: https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/#application-factories
[sample-flask-project]: https://git.teko.vn/quy.nt/sqlalchemy-tutorial/-/blob/master/flaskr/__init__.py
## Initialize sqlite database
>$ ./scripts/init_db.sh
## Drop sqlite database
Either delete the sqlite file, or run this command
>$ ./scripts/drop_db.sh
## Style python code
>$ ./scripts/autopep8.sh
## Run test
>$ ./scripts/test.sh
## Synchronous connection between master and slave app
>When insert/update user or resume into the master app's database, the master app will send http requests to the slave app, so that the slave can sync its database with the master's database.
>
>The slave app is located in branch `slave`, run its on port 4000 with `flask run --port 4000`.
## Asynchronous connection between master and slave app
>When insert/update user or resume into the master app's database, the master app will send message to the message broker (`Apache Kafka`).
>
>Upon receiving messages sent by the master app (`producer`), the message broker send message to `consumer` `flask` app.
>
>The consumer then send `http` request to the `slave` app so that the `slave` app can update its database followed the `master`
>
>The `master` app is located in branch `async_master`
