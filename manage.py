'''Management commands.'''

import os
from flask.ext.script import Manager
from wall import app, db, models
from flask.ext.migrate import Migrate, MigrateCommand
import datetime

manager = Manager(app)
app.config.from_object('config.BaseConfiguration')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def createdb():
    '''Runs the db init, db migrate, db upgrade commands automatically'''
    os.system('python manage.py db init')
    os.system('python manage.py db migrate')
    os.system('python manage.py db upgrade')
    ci = models.ContinuousBuilds(
    name = 'JOB-Tests',
    number = 1,
    phase =  'STARTED',
    status =  '',
    sourceBranch =  'feature',
    targetBranch = 'pilot',
    full_url = 'http://jenkins:8080/job/JOB-TESTS/1/',
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    deployPilot = models.Deployments(
    name = 'JOB-Pilot',
    number = 1,
    phase =  'STARTED',
    status =  '',
    sourceBranch =  'pilot',
    full_url = 'http://jenkins:8080/job/JOB-Pilot/1/',
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    deployProd = models.Deployments(
    name = 'JOB-Prod',
    number = 1,
    phase =  'FINALIZED',
    status =  'SUCCESS',
    sourceBranch =  'master',
    full_url = 'http://jenkins:8080/job/JOB-Prod/1/',
    date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    date_modified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(ci)
    db.session.add(deployPilot)
    db.session.add(deployProd)
    db.session.commit()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)


@manager.command
def lint():
    '''Lints the codebase'''
    command = 'flake8 --ignore E127,E221,F401 --max-line-length=220 --exclude=db_repository,tests,env,migrations .'
    os.system(command)


@manager.command
def clean():
    '''Cleans the codebase'''
    commands = ["find . -name '*.pyc' -exec rm -f {} \;",
                "find . -name '*.pyo' -exec rm -f {} \;",
                "find . -name '*~' -exec rm -f {} \;",
                "find . -name '__pycache__' -exec rmdir {} \;", "rm -f app.db",
                "rm -rf migrations", "rm -f wall.log"]
    for command in commands:
        os.system(command)


if __name__ == "__main__":
    manager.run()

