from colinthecomputer.utils import make_path
from colinthecomputer.utils import filtered_dict

from PIL import Image
from pathlib import Path
import json
import os


def parse_color_image(data, directory=os.environ['BLOB_DIR'] + '/results'):
    """Parse color image from snapshot data, save BLOB to fs.
    
    :param data: snapshot as consumed from the message queue
    :type data: json
    :returns: parsed snapshot color image, with a path to the parsed binary data
    :rtype: json
    """
    directory = Path(directory)
    data = json.loads(data)
    # Create parsed metadata json
    color_image = filtered_dict(data, ['user_id', 'datetime'])
    path = directory / str(color_image['user_id']) / color_image['datetime']
    if not path.exists():
         path.mkdir(parents=True)
    path /= 'color_image.jpg'
    color_image['data'] = {'path': str(path)}

    # Save parsed image to filesystem
    data = data['color_image']
    with open(data['data'], 'rb') as file:
        result = Image.frombytes('RGB', (data['width'], data['height']), file.read()) 
    result.save(path)
    return json.dumps(color_image)

parse_color_image.field = 'color_image'