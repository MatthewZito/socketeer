from os.path import abspath

ROOT_SCRIPTS_DIR = abspath('scripts')
GET_LATEST = 'get_latest.sh'
COMMIT_SHA = '.commit_id'
TASK_RESULTS = '.task_results'

INTERVAL = 20

MESSAGES = {
	'DISPATCH': 'DISPATCH',
	'STATUS': 'STATUS',
	'RESPONSE': 'RESPONSE',
	'REGISTER': 'REGISTER',
	'OK': 'OK',
	'DELIMITER': ':'
}