from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from seaflow.main.exts import db
from run import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
    """迁移：python manage.py db init(第一次迁移)
            python manage.py db upgrade
    回滚：python manage.py db downgrade 版本号
    历史版本：python manage.py db history
                                """
