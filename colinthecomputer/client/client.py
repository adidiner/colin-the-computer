import time

'''from colinthecomputer.protocol import Connection
from colinthecomputer.client.reader import Reader
from colinthecomputer.protocol import User, Config, Snapshot'''

import colinthecomputer.protocol as ptc
import colinthecomputer.client.reader as rd

def upload_sample(path, *, host='127.0.0.1', port=8000, file_format='protobuf'):
    """Uploads sample from given path to the server.

    :param path: path to the sample file
    :type path: str
    :param host: server host address, defaults to 127.0.0.1
    :type host: str, optional
    :param port: server port address, defaults to 8000
    :type port: str, optional
    :param file_format: the sample file format, supported formats are binary and protobuf.
     defaults to protobuf
    :type file_format: str, optional
    """
    reader = rd.Reader(path, file_format)
    for snapshot in reader:
        try:
            with ptc.Connection.connect(host, port) as connection:
                send_hello(connection, reader.user)
                config = receive_config(connection)
                send_snapshot(connection, config, snapshot)
        except Exception as error:
            print(f"ERROR in {__name__}: {error}")
            break
        #time.sleep(0.2)  # TODO: figure out threading problem


def send_hello(connection, hello):
    """Sends hello message to a server.

    :param connection: connection object to the server
    :type connection: Connection
    :param hello: hello message
    :type hello: User
    """
    message = hello.SerializeToString()
    connection.send_message(message)


def receive_config(connection):
    """Recieves config message from a server.

    :param connection: connection object to the server
    :type connection: Connection
    :return: the received config message
    :rtype: Config
    """
    message = connection.receive_message()
    config = ptc.Config()
    config.ParseFromString(message)
    return config


def send_snapshot(connection, config, snapshot):
    """Sends snapshot message to a server, including only the fields specifed in config.
    :param connection: connection object to the server
    :type connection: Connection
    :param config: config sepcifing the required fields
    :type config: Config
    :param snapshot: snapshot to be sent
    :type snapshot: Snapshot
    """
    fields = {field: snapshot[field] for field in config}
    snapshot = ptc.Snapshot(datetime=snapshot.datetime, **fields)
    message = snapshot.SerializeToString()
    connection.send_message(message)
