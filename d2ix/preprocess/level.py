import logging

from d2ix import RawData

logger = logging.getLogger(__name__)


def process_level(_data: RawData) -> dict:
    df = _data['base_input']['level'].copy()
    df = df.set_index('level_type')

    data = {}
    for index, row in df.iterrows():
        data[index] = row['level']

    logger.debug('Created helper data structure: \'level\'')
    return data
