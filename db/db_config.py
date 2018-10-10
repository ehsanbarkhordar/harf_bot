import os


class DatabaseConfig:
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('POSTGRES_USER', "ehsan"),
                                      os.environ.get('POSTGRES_PASSWORD', "ehsan1379"),
                                      os.environ.get('POSTGRES_HOST', "localhost"),
                                      os.environ.get('POSTGRES_PORT', "5432"),
                                      os.environ.get('POSTGRES_DB', "harfbeman"))
