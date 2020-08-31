from seaflow.main import create_app
from config import DevelopmentConfig
from seaflow.models.auth import create_role
from seaflow import io

app = create_app(DevelopmentConfig)
app.app_context().push()

if __name__ == '__main__':
    io.run(app, host='0.0.0.0', port=5000, debug=True)
    # app.run(port=8080, debug=True)
