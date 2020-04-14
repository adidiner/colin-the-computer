from colinthecomputer.protocol import User, Config, Snapshot, Pose, ColorImage, DepthImage, Feelings


_USER_ID = 49
_USERNAME = 'Adi Dinerstein'
_BIRTH_TIMESTAMP = 974239200
_GENDER = 1

_COLOR_IMAGE = ColorImage(width=10, 
                          height=20, 
                          data=b'0'*20*10*3)
_DEPTH_IMAGE = DepthImage(width=5, 
                          height=7, 
                          data=b'0'*7*5*4)
_POSE1 = Pose(translation=Pose.Translation(x=1.0, y=2.0, z=3.0),
              rotation=Pose.Rotation(x=1.0, y=2.0, z=3.0, w=4.0))
_POSE2 = Pose(translation=Pose.Translation(x=0.5, y=3.0, z=4.0),
              rotation=Pose.Rotation(x=3.0, y=3.0, z=3.0, w=3.0))
_FEELINGS1 = Feelings(hunger=-0.5,
                      thirst=-0.125,
                      exhaustion=-0.5,
                      happiness=0.5)
_FEELINGS2 = Feelings(hunger=0.5,
                      thirst=0.125,
                      exhaustion=1.0,
                      happiness=-0.5)
_SNAPSHOT1 = Snapshot(datetime=1576237612000,
                      pose=_POSE1,
                      color_image=_COLOR_IMAGE, 
                      depth_image=_DEPTH_IMAGE,
                      feelings=_FEELINGS1)
_SNAPSHOT2 = Snapshot(datetime=1576237618000, 
                      pose=_POSE2,
                      color_image=_COLOR_IMAGE, 
                      depth_image=_DEPTH_IMAGE,
                      feelings=_FEELINGS2)


SAMPLE = 'test_sample.mind'
USER = User(user_id=_USER_ID,
             username=_USERNAME,
             birthday=974239200,
             gender=_GENDER)
SNAPSHOTS = [_SNAPSHOT1, _SNAPSHOT2]
CONFIG = Config(fields=['pose', 
                        'color_image', 
                        'depth_image', 
                        'feelings'])