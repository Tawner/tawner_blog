from apps import create_app
import os
app, manager = create_app(os.getenv('FLASK_CONFIG') or 'development')


if __name__ == '__main__':
    manager.run()
