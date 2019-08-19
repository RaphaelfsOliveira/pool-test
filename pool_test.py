config = {
    'name': 'markII',
    'size': 3,
    'max_size': 5,
    'conn_timeout': 10,
    'conn_max_time': 15,
    'user': 'admin',
    'password': 1234,
    'host': 'localhost',
    'database': 'opa'
}

class Connection(object):
    def __init__(self, user, password, host, database, active=False):
        self.db_user = user
        self.db_password = password
        self.db_host = host
        self.db_database = database
        self.active = active

class Pool(object):
    def __init__(self, name, size, max_size, conn_timeout,
                 conn_max_time, user, password, host, database):
        self.db_user = user
        self.db_password = password
        self.db_host = host
        self.db_database = database

        self.name = name
        self.size = size
        self.max_size = max_size
        self.conn_timeout = conn_timeout
        self.conn_max_time = conn_max_time

        self.connections = []
        self.active_connections = []
        self.conn_id = 0

        self.init_default_connections()

    def init_default_connections(self):
        for size in range(self.size):
            self.create_connection()

    def connection(self):
        conn = Connection(user=self.db_user,
                          password=self.db_password,
                          host=self.db_host,
                          database=self.db_database)
        conn_pooled = {
            'pool': self.name,
            'conn_name': '{}_{}_{}'.format(self.name, 'conn', self.conn_id),
            'connection': conn
        }
        self.conn_id += 1
        return conn_pooled

    def get_connection(self):
        if len(self.connections) > 0:
            conn = self.connections.pop()
            conn['connection'].active=True

            self.reset_connection(conn)

    def create_connection(self):
        if len(self.connections) < self.max_size:
            conn = self.connection()
            self.connections.append(conn)
            return self.connection()
        else:
            raise Exception('the maximum number of connections has been exceeded')

    def reset_connection(self, conn):
        conn['connection'].active=False
        self.connections.append(conn)

    def destroy_connection(self):
        for i, conn in enumerate(self.connections):
            if len(self.connections) > self.size and not conn['connection'].active:
                del self.connections[i]
