import pathlib
import threading
import os
import numpy as np
import queue

import colinthecomputer.protocol as ptc
from colinthecomputer.utils import printerr

HEADER_SIZE = 20
DIRECTORY = os.environ['BLOB_DIR'] \
            if 'BLOB_DIR' in os.environ else 'colinfs'
DATA_HANDLERS = 30

run = True
tasks = queue.Queue()


class DataHandler(threading.Thread):
    """
    Handles data from clients, consumed from the task queue.

    :param publish: publishing function (for client message)
    :type publish: callable
    """
    def __init__(self, publish):
        super().__init__()
        self.daemon = True
        self.publish = publish

    def __del__(self):
        self.alive = False

    @printerr
    def run(self):
        """
        Use self.publish to publish the snapshot,
        when converting to json before publishing.
        BLOBS are stored in the fs, with only their path being published.
        """
        while True:
            user, snapshot = tasks.get()
            user_id = user.user_id
            # Save BLOBs to filesystem
            path = \
                pathlib.Path(DIRECTORY) / 'raw_data' \
                / str(user_id) / str(snapshot.datetime)
            paths = self._save_binary(path, snapshot)
            color_path, depth_path = paths
            # Create slim to-publish json messages
            user = ptc.json_user_message(user)
            snapshot = ptc.json_snapshot_message(snapshot, user_id,
                                                 color_image_path=color_path,
                                                 depth_image_path=depth_path)
            self.publish((user, snapshot))
            tasks.task_done()

    @staticmethod
    def _save_binary(path, snapshot):
        """
        Saves binary blobs to a given path.
        """
        path.mkdir(parents=True, exist_ok=True)
        color, depth = path / 'color_image', path / 'depth_image.npy'
        color.write_bytes(snapshot.color_image.data)
        depth_image_data = np.array(snapshot.depth_image.data)
        np.save(depth, depth_image_data)
        return str(color), str(depth)


class ConnectionHandler(threading.Thread):
    """
    Handels a single connection from client.

    :param client: client connection
    :type client: Connection
    """
    def __init__(self, client):
        super().__init__()
        self.client = client

    @printerr
    def run(self):
        """
        Run handler, communicating in hello -> snapshot protocol.
        Upload data to task queue.
        """
        with self.client:
            # Receive hello
            data = self.client.receive_message()
            # Sometimes I just want to easily kill the server,
            # this is not an infosec course
            if data == b'kill':
                global run
                run = False
                return
            user = ptc.User()
            user.ParseFromString(data)
            # Receive snapshot
            data = self.client.receive_message()
            snapshot = ptc.Snapshot()
            snapshot.ParseFromString(data)
        tasks.put((user, snapshot))


@printerr
def run_server(host='0.0.0.0', port=8000, publish=print):
    """
    Run server, which starts a listner and handles
    every client connection in a new thread.

    :param host: server's host, defaults to '127.0.0.1'
    :type host: str, optional
    :param port: server's port, defaults to 8000
    :type port: int, optional
    :param publish: publishing function to incoming snapshots,
                    defaults to printing to STDOUT
    :type publish: callable, optional
    """
    # Start data handlers to process client data
    for _ in range(DATA_HANDLERS):
        handler = DataHandler(publish)
        handler.start()

    try:
        # Setup server
        with ptc.Listener(host=host, port=port) as server:
            while run:
                # Recieve message
                client = server.accept()
                handler = ConnectionHandler(client)
                handler.start()

    finally:
        tasks.join()
