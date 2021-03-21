from os.path import abspath

ROOT_SCRIPTS_DIR = abspath('scripts')
GET_LATEST = 'get_latest.sh'
PRE_TASK = 'pre_task.sh'
COMMIT_SHA = '.commit_id'
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
	'ACK': 'ACK'
}