from seaflow.main import create_app
from config import DevelopmentConfig
from seaflow.models.auth import create_role
create_role()
app = create_app(DevelopmentConfig)
app.app_context().push()


if __name__ == '__main__':
    app.run(port=8080, debug=True)
