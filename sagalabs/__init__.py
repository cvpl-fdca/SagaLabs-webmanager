import os
from flask import Flask
from sagalabs import sagalabs


def create_app(test_config=None, instance_relative_config=True):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'sagalabs.db.sqlite3'),
        SECRET_KEY='s3cret'
    )
    # app.secret_key = 's3cret'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        print("Instance folder: ", app.instance_path)
    except OSError as e:
        # How to properly handle this?
        # On first ever request to the app folders are created,
        # on subsequent requests the folders already exist.
        pass

    from . import db
    db.init_app(app)

    app.register_blueprint(sagalabs.bp)

    return app
