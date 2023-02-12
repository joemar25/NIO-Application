''''
    this generator file contains all the generator classes for returning [Score(s), File, ...]

    - Score: contains rate (speed), pitch, articulation, prounounciation, volume
        which includes Feedback, depending on the generated scores

    - File : contains the generated filename. Used for saving a file.
'''

__authors__ = "joemar_olan_glenn_arrlee_jericho"
__version__ = "1.1"
__docformat__ = "restructuredtext en"

try:
    import os
    import uuid
    import pytz
    from datetime import datetime
    from gingerit.gingerit import GingerIt
except ImportError as e:
    print(e)
    raise

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Score:
    pass


class File:

    def generated_name() -> str:
        # uses: uuid, pytz, datetime
        todays: datetime = datetime.now(pytz.timezone('Asia/Manila')).utcnow()
        utime: str = f'{uuid.uuid1()}{todays.hour}{todays.minute}{todays.second}'

        deduct: int = -2 if str(todays.year)[1] == '0' else -3
        udate: str = f"{str(todays.year)[deduct:]}{todays.month}{todays.day}"

        return f"{udate}{utime}"

    # def files_from_dataset(self, file_type) -> list:

    #     # add error handling
    #     file_list = []
    #     # get the directory above current directory then go to \audio\dataset
    #     path = os.path.abspath(os.path.join(
    #         os.getcwd(), os.pardir)) + '\\audio\\dataset'
    #     print("Current path:", path)
    #     for root, dirs, files in os.walk(path):
    #         for file in files:
    #             if file[-3:] == file_type:
    #                 file_list.append(os.path.join(root, file))
    #     return file_list
