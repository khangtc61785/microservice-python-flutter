from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Posgressql():
    def __init__(self, host, port, db_name, username, password):
        # [TODO] Validate
        self.engine, self.connection = self.__connect(host, port, db_name, username, password)
        self.session = sessionmaker(bind=self.engine)

    def __connect(self, host, port, db_name, username, password):
        engine = create_engine('postgresql://{}:{}@{}/{}'.format(
            username, password, host, db_name
        ))
        connection = engine.connect()
        return engine, connection

    def disconnect(self):
        self.connection.close()
        self.engine.dispose()

