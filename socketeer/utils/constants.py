from os.path import abspath

COMMIT_SHA = '.commit_id'
GET_LATEST = 'get_latest.sh'
PRE_TASK = 'pre_task.sh'
ROOT_SCRIPTS_DIR = abspath('scripts')
TASK_RESULTS = '.task_results'
TMP_RESULTS = 'tmp_results'

INTERVAL = 20
RANGE_INIT = 9900

MESSAGES = {
    'DISPATCH': 'DISPATCH',
    'STATUS': 'STATUS',
    'RESPONSE': 'RESPONSE',
    'REGISTER': 'REGISTER',
    'OK': 'OK',
    'DELIMITER': ':',
    'ACK': 'ACK',
    'PING': 'PING',
    'RUNTASK': 'RUNTASK'
}
