#!/usr/bin/env python -i
import os
import sys

PYTAN_PATH = '~/gh/pytan'
PYTAN_PATH = os.path.expanduser(PYTAN_PATH)
sys.path.insert(0, PYTAN_PATH)

my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
pytan_root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, pytan_root_dir)

try:
    import pytan  # noqa
except Exception as e:
    print("ERROR: Unable to import pytan package, error: '{}'".format(e))
    print("Full PYTHONPATH: {}".format(', '.join(sys.path)))
    sys.exit(99)

if __name__ == "__main__":
    worker_module = "pytan.shell.pytan_shell"

    __import__(worker_module)
    module = eval(worker_module)
    worker = module.Worker()

    console = worker.interactive_check()
    check = worker.check()
    setup = worker.setup()
    args = worker.parse_args()
    handler = worker.get_handler()
    result = worker.get_result()
    exec(worker.get_exec())


from pytan.utils import write_file
os.chdir(my_dir)


def write_last_response(t, n, ext='xml'):
    fn = '{}_{}_raw.{}'.format(t, n.replace('.*', '...'), ext)
    print(write_file(fn, handler.SESSION.LAST_RESPONSE.text))


def do_q(q):
    v = handler.ask_parsed(question_text=q, picker=1)
    handler.get_result_data(v.question_object)
    write_last_response('resultdata', q)
    handler.get_result_info(v.question_object)
    write_last_response('resultinfo', q)
    handler.get_result_data(v.question_object, sse=True)
    write_last_response('resultdata_sse', q)


n = 'Action Statuses'
e = {'value': n}
v = handler.get_sensors(e)
write_last_response('sensors', n)

n = 'Computer Name'
e = {'value': n}
v = handler.get_sensors(e)
write_last_response('sensors', n)

n = 'Tanium Action Log'
e = {'value': n}
v = handler.get_sensors(e)
write_last_response('sensors', n)

n = 'Operating System.*Directory'
e = {'value': n, 'operator': 're'}
v = handler.get_sensors(e)
write_last_response('sensors', n)

n = 'Last 20 minutes of questions'
e = {
    'value': pytan.tickle.tools.secs_from_now(secs=-(60 * 20)),
    'type': 'Date',
    'field': 'expiration',
    'operator': 'Greater',
}
v = handler.get_questions(e)
write_last_response('questions', n)

n = 'id 1'
o = pytan.tanium_ng.User(values={'id': 1})
handler.SESSION.find(o)
write_last_response('user', n)

n = 'Administrator'
e = {'value': n}
v = handler.get_users(e)
write_last_response('users', n)

n = 'Last 20 minutes of actions'
e = {
    'value': pytan.tickle.tools.secs_from_now(secs=-(60 * 20)),
    'type': 'Date',
    'field': 'expiration_time',
    'operator': 'Greater',
}
v = handler.get_actions(e)
if not v:
    raise Exception('no actions deployed in last 20 minutes, deploy one!')
write_last_response('actions', n)

do_q('Computer Name')
do_q('Computer Name and IP Address')
do_q('Computer Name and IP Route Details')
do_q('Computer Name and IP Route Details and Installed Applications')
do_q('IP Route Details and Installed Applications')
