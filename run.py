from seaflow.main import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)
app.app_context().push()
print(app.url_map)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
