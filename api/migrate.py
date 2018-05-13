from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from models import db
from run import app


def make_shell_context():
    return dict(app=app, db=db)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
