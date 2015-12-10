#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4 softtabstop=1 shiftwidth=4 expandtab:
# Please do not change the two lines above. See PEP 8, PEP 263.


import os
import sys
sys.dont_write_bytecode = True
my_file = os.path.abspath(sys.argv[0])
my_dir = os.path.dirname(my_file)
sys.path.append(my_dir)

from config import config
import common

sys.path.append(config['pytan_dir'])

import pytan
import cgi
import traceback


def json_print_end(ret, error=False, finished=False):
    if error:
        ret['error'] = True
        ret['finished'] = True
    if finished:
        ret['finished'] = True
    common.print_html(pytan.utils.jsonify(ret))
    sys.exit()


def add_status(ret, s, next=False):
    if 'status' not in ret:
        ret['status'] = []
    if type(ret['status']) not in [list, tuple]:
        ret['status'] = [ret['status']]
    ret['status'].append("[{}] [STEP 3-{}] {}".format(pytan.utils.get_now(), ret['substep'], s))
    if next:
        ret['substep'] += 1
    return ret


def die(ret, s, error=True):
    ret = add_status(ret, "ERROR: {}".format(s))
    json_print_end(ret, error)


def add_job(ret, j):
    if 'jobs' not in ret:
        ret['jobs'] = []
    if type(ret['jobs']) not in [list, tuple]:
        ret['jobs'] = [ret['jobs']]
    ret['jobs'] = [x for x in ret['jobs'] if x]
    if type(j) in [tuple, list]:
        for i in j:
            if i not in ret['jobs'] and i:
                ret['jobs'].append(str(i))
    else:
        if j not in ret['jobs'] and j:
            ret['jobs'].append(str(j))
    return ret


def get_jobs(ret, formdict):
    jobs = formdict.get('jobs', [])

    if not jobs:
        die(ret, "No jobs supplied!")

    if type(jobs) not in [list, tuple]:
        jobs = [jobs]
    return jobs


def ask_question(handler, computer_id, formdict, ret, sensors):
    kwargs = {
        'qtype': 'manual_human',
        'sensors': sensors,
        'question_filters': 'Computer ID, that =:{}'.format(computer_id),
        'get_results': False,
    }
    ask_ret = handler.ask(**kwargs)
    question_obj = ask_ret['question_object']
    m = "Asked question '{}', ID: {}".format
    ret = add_status(ret, m(question_obj.query_text, question_obj.id), next=True)
    ret = add_job(ret, question_obj.id)
    ret['pytan_args'] = kwargs
    return ret


def check_question(handler, computer_id, formdict, ret, job):
    ret['retry'] = int(formdict.get('retry', 1))
    try:
        question_obj = handler.get('question', id=job)[0]
    except:
        die(ret, "Unable to find question ID {}".format(job))

    result_info = handler.session.getResultInfo(question_obj)
    tested_pct = result_info.mr_tested * 100
    estimated_total_pct = result_info.estimated_total + .01
    new_pct = tested_pct / estimated_total_pct
    ret['data_ready'] = False
    if new_pct >= config['pct_complete_threshold']:
        m = "Question ID {0}, '{1}' status: Results Finished.. {2:.0f}%  complete".format
        ret = add_status(ret, m(question_obj.id, question_obj.query_text, new_pct))
        ret['data_ready'] = True
        result_data = handler.session.getResultData(question_obj)

        csv_out = handler.export_obj(result_data, 'csv')
        m = "Question ID {0}, VERBOSE: CSV OUTPUT:\n{1}".format
        ret = add_status(ret, m(question_obj.id, csv_out))

        ret['results'] = common.rd_dict(result_data)

        if not ret['results']:
            if ret['retry'] >= config['max_question_data_retry']:
                m = "No results found for Question ID {0}, '{1}'!".format
                die(ret, m(question_obj.id, question_obj.query_text))
            else:
                m = (
                    "Question ID {0}, '{1}' status: Retrying results #{2}.. {3:.0f}%  complete"
                ).format
                ret = add_status(
                    ret,
                    m(question_obj.id, question_obj.query_text, ret['retry'], new_pct)
                )
                ret['retry'] += 1
                ret['data_ready'] = False
    else:
        m = "Question ID {0}, '{1}' status: Waiting for results.. {2:.0f}%  complete".format
        ret = add_status(ret, m(question_obj.id, question_obj.query_text, new_pct))
    return ret


def deploy_action(handler, computer_id, package, ret, next=True):
    kwargs = {
        'package': package,
        'action_filters': [
            'Computer ID, that =:{}'.format(computer_id),
            # 'Online, that =:True',
        ],
        'run': True,
        'get_results': False,
    }

    # OVERCOME THE 'aid' error from tanium
    retry = 1
    max_retry = 5
    action_obj = None
    while retry <= max_retry:
        try:
            action_obj = handler.deploy_action_human(**kwargs)['action_object']
            break
        except:
            m = "VERBOSE: Add action retry #{}, caught exception: {}".format
            ret = add_status(ret, m(retry, traceback.format_exc()))
            retry += 1

    m = "Deployed Action '{}'' (id: {})".format
    ret = add_status(ret, m(action_obj.name, action_obj.id), next)
    ret = add_job(ret, action_obj.id)
    ret['pytan_args'] = kwargs
    return ret


def check_action(handler, formdict, ret, job):
    ret['action_done'] = False

    try:
        action_obj = handler.get('action', id=job)[0]
    except:
        m = "Unable to find action ID {}".format
        die(ret, m(job))

    rd = handler.get_result_data(action_obj, True)
    if not rd.rows:
        ret['action_status'] = "Waiting to download."
    else:
        ret['action_status'] = rd.rows[0]['Action Statuses'][0].split(':')[1]

    full_status = "Action ID {}, '{}' status: {}".format
    ret = add_status(ret, full_status(action_obj.id, action_obj.name, ret['action_status']))
    if 'completed' in ret['action_status'].lower():
        ret['action_done'] = True
    elif 'failed' in ret['action_status'].lower():
        ret['error'] = True
    return ret


def create_get_pkg(handler, ret, pkg_name, pkg_opts):
    try:
        p = handler.get('package', name=pkg_name)[0]
        m = 'Found package {}, skipped creation'.format
        ret = add_status(ret, m(pkg_name))
    except:
        p = handler.create_package(name=pkg_name, **pkg_opts)
        m = 'Created package {}'.format
        ret = add_status(ret, m(pkg_name))
    # TODO: Add validation that pkg_opts == p attrs, update if not
    return ret, p


def create_get_patch_pkg(handler, ret, rd_row):
    pkg_name = config['patchpkg_name'](**rd_row)
    pkg_opts = {}
    file_names = rd_row['Filename'].split(',')
    file_urls = rd_row['Download'].split(',')
    pkg_opts['file_urls'] = ["{}||{}".format(x, y) for x, y in zip(file_names, file_urls)]
    pkg_opts['metadata'] = [list(i) for i in rd_row.items() if 'Status' not in i[0]]
    pkg_opts.update(config['patchpkg_opts'])
    ret, p = create_get_pkg(handler, ret, pkg_name, pkg_opts)
    return ret, p


def deploy_patch_pkg(handler, computer_id, ret, rd_row):
    pkg_name = config['patchpkg_name'](**rd_row)
    ret = deploy_action(handler, computer_id, pkg_name, ret, False)
    return ret


def wipe_all_managed_patch_pkgs(handler):
    a = [
        handler.delete('package', id=v.id)
        for v in handler.get_all('package')
        if v.name.startswith('Managed Windows Patch Deployment')
    ]
    return a


def main(ret):
    # get the form submission
    form = cgi.FieldStorage()

    formdict = common.formtodict(form)

    # BOOTSTRAP TESTS
    # formdict['computer_id'] = '1987595770'
    # formdict['substep'] = "11"
    # formdict['jobs'] = ["18372"]

    computer_id = formdict.get('computer_id', "")
    substep = int(formdict.get('substep', 0))

    ret['substep'] = substep
    ret['computer_id'] = computer_id

    if not computer_id:
        die(ret, "Missing computer_id!")

    try:
        # connect to Tanium
        handler = pytan.Handler(
            username=config['tanium_username'],
            password=config['tanium_password'],
            host=config['tanium_host'],
        )
    except Exception as e:
        jobs = get_jobs(ret, formdict)
        ret = add_job(ret, jobs)
        die(ret, "Unable to connect to Tanium: {}!".format(e), False)

    if substep == 1:
        '''
        Ask the question Get Computer Name for this computer_id
        '''
        ret = ask_question(handler, computer_id, formdict, ret, 'Computer Name')
    elif substep == 2:
        '''
        Get the results of previous question, if data ready add computer name to return dict
        for consumption by calling javascript
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_question(handler, computer_id, formdict, ret, job)
        if ret['data_ready'] and ret['results']:
            ret['computer_name'] = ret['results'][0]['Computer Name']
            m = "Found computer name {} for computer ID {}".format
            ret = add_status(ret, m(ret['computer_name'], computer_id), next=True)
            # ret['substep'] = 10  # BOOTSTRAP

    elif substep == 3:
        '''
        Deploy the action "Distribute Patch Tools"
        '''
        ret = deploy_action(handler, computer_id, "Distribute Patch Tools", ret)
    elif substep == 4:
        '''
        Check if previous action done, go to next step if so
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]

        ret = add_job(ret, job)
        ret = check_action(handler, formdict, ret, job)
        if ret['action_done']:
            ret['substep'] += 1
    elif substep == 5:
        '''
        Check that sync scan pkg exists, create if not
        '''
        ret, pkg = create_get_pkg(handler, ret, config['sync_scan_name'], config['sync_scan_opts'])
        ret['substep'] += 1
    elif substep == 6:
        '''
        Deploy the action "Run Patch Scan Synchronously"
        '''
        ret = deploy_action(handler, computer_id, config['sync_scan_name'], ret)
    elif substep == 7:
        '''
        Check if previous action done, go to next step if so
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_action(handler, formdict, ret, job)
        if ret['action_done']:
            ret['substep'] += 1
    elif substep == 8:
        '''
        Ask the question Get Tanium Action Log for previous action for this computer_id
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]

        sensors = 'Tanium Action Log{{actionNumber={}}}'.format(job),
        ret = ask_question(handler, computer_id, formdict, ret, sensors)
    elif substep == 9:
        '''
        Get the results of previous question, if data ready and patch scan finished, go to next step
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_question(handler, computer_id, formdict, ret, job)
        if ret['data_ready'] and ret['results']:
            lines = sorted([x.values()[0] for x in ret['results']])
            log_output = '\n'.join(lines)
            m = "VERBOSE: Tanium Action Log contents finish:\n{}".format
            ret = add_status(ret, m(log_output))

            did_not_run = "patch scan currently running"
            scan_done = "finished running patch scan"
            max_lines = "max number of lines reached"

            if did_not_run in log_output.lower():
                m = 'Re-running patch scan, one already running'
                ret = add_status(ret, m)
                ret['substep'] = 6
            elif scan_done in log_output.lower() or max_lines in log_output.lower():
                m = 'Patch scan finished, getting available patches'
                ret = add_status(ret, m, next=True)
    elif substep == 10:
        '''
        Ask the question Get Available Patches for this computer_id
        '''
        ret = ask_question(handler, computer_id, formdict, ret, 'Available Patches')
    elif substep == 11:
        '''
        Get the results of previous question,
        if data ready and no available patches, go to step 14
        if data ready and available patches, create pkgs for each patch and go to next step
        if data ready and current results unavailable (??) re-ask the question
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_question(handler, computer_id, formdict, ret, job)
        if ret['data_ready']:
            ret['results'] = common.remove_noresults(ret['results'])
            if ret['results']:
                title = ret['results'][0]['Title']
                # TODO: DO THIS BETTER
                if 'current results unavailable' in title.lower():
                    m = "Re-asking due to {}".format
                    ret = add_status(ret, m(title))
                    ret['substep'] = 10
                elif 'all available patches queued for installation' in title.lower():
                    ret = add_status(ret, title, next=True)
                    ret['substep'] = 14
                else:
                    m = "Retrieved {} available patches".format
                    ret = add_status(ret, m(len(ret['results'])), next=True)
                    for rd_row in ret['results']:
                        ret, pkg = create_get_patch_pkg(handler, ret, rd_row)
            else:
                m = "No available patches to deploy"
                ret = add_status(ret, m)
                ret['substep'] = 14
    elif substep == 12:
        '''
        Get the results of previous question,
        if data ready and available patches, deploy pkgs for each patch
        '''
        jobs = get_jobs(ret, formdict)
        job = jobs[0]

        ret = check_question(handler, computer_id, formdict, ret, job)
        if ret['data_ready']:
            if ret['results']:
                for rd_row in ret['results']:
                    ret = deploy_patch_pkg(handler, computer_id, ret, rd_row)
                ret['substep'] += 1
    elif substep == 13:
        '''
        Get the results of each previous deploy patch pkg,
        if all actions finished, go to next step
        '''
        jobs = get_jobs(ret, formdict)
        ret = add_job(ret, jobs)
        done_list = []

        for job in jobs:
            ret = check_action(handler, formdict, ret, job)
            done_list.append(ret['action_done'])

        if all(done_list):
            m = "All {} patch packages have finished deploying".format
            ret = add_status(ret, m(len(done_list)), True)
        else:
            m = "VERBOSE: {} patch packages have finished deploying out of {}".format
            ret = add_status(ret, m(len([x for x in done_list if x]), len(jobs)))
    elif substep == 14:
        ret = ask_question(handler, computer_id, formdict, ret, 'Has Patch Files')
    elif substep == 15:
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_question(handler, computer_id, formdict, ret, job)
        ret['results'] = common.remove_noresults(ret['results'])
        if ret['data_ready'] and ret['results']:
            has_patch_files = ret['results'][0]['Has Patch Files']
            if 'yes' in has_patch_files.lower():
                m = "Patch files exist that need to be deployed".format
                ret = add_status(ret, m(), next=True)
            else:
                m = "No patch files exist that need to be deployed, patch process finished".format
                ret = add_status(ret, m())
                ret['finished'] = True

    elif substep == 16:
        ret = deploy_action(handler, computer_id, "Install Deployed Patches", ret)
    elif substep == 17:
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_action(handler, formdict, ret, job)
        if ret['action_done']:
            ret['substep'] += 1
    elif substep == 18:
        ret = ask_question(handler, computer_id, formdict, ret, 'Has Patch Files')
    elif substep == 19:
        jobs = get_jobs(ret, formdict)
        job = jobs[0]
        ret = add_job(ret, job)

        ret = check_question(handler, computer_id, formdict, ret, job)
        ret['results'] = common.remove_noresults(ret['results'])
        if ret['data_ready'] and ret['results']:
            has_patch_files = ret['results'][0]['Has Patch Files']
            if 'yes' in has_patch_files.lower():
                m = "Patch files still exist, Install Deployed Patches must still be running"
                ret = add_status(ret, m)
                ret['substep'] = 18
            else:
                m = "No patch files exist, Install Deployed Patches must be finished"
                ret = add_status(ret, m, next=True)
    # elif substep == 20:
    #     ret = deploy_action(handler, computer_id, "Reboot Windows Machine", ret)
    # elif substep == 21:
    #     jobs = get_jobs(ret, formdict)
    #     job = jobs[0]
    #     ret = add_job(ret, job)

    #     ret = check_action(handler, formdict, ret, job)
    #     if ret['action_done']:
    #         ret['substep'] += 1

        '''
        How to determine Install Deployed Patches == Finished (Just Has Patch Files == No?)
        How to determine reboot is done?
1) best way to see if Installed Deployed Patches is finished is if the "Patches deployed by Tanium" sensor returns what you tried to deploy

greg_smith [9:37 AM]
or if Installed patches returns what you deployed

greg_smith [9:38 AM]
I would pick those, as you definitely know it finished and was a success in those cases

greg_smith [9:38 AM]
2)  You can use boot time (its something like that, maybe last reboot time, not sure)

greg_smith [9:38 AM]9:38
when it changes to 5 minutes ago, you know the machine rebooted and is back online
        go back to 6
        '''
    else:
        die(ret, "Invalid substep {}!".format(substep))

    json_print_end(ret)
    return


ret = {
    'status': [],
    'error': False,
    'finished': False,
    'substep': '-1',
    'jobs': [],
    'formdict': False,
    'results': [],
}

try:
    main(ret)
except Exception as e:
    die(ret, "Exception {}!".format(traceback.format_exc()))
