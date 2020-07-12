from seaflow.main import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)
if __name__ == '__main__':
    app.run(port=8080)
