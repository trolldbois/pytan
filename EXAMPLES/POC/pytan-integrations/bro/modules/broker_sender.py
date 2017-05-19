# -*- coding: utf-8 -*-
"""Provides class to send pytan data to Bro via broker
"""

###############################################################################
# WARNING BROKER IS BEING REWRITTEN THIS SENDER MAY NOT WORK AFTER VERSION 0.6
#   This code should be used as a jump point to feed data from pytan to a bro
# box.
###############################################################################
from datetime import datetime
from select import select

import pybroker  # Requires broker python bindings compiled.
import flatten


class TaniumBrokerSender(object):
    """Creates a connection via Broker API and sends a message.

    Args:
        dst_host (str OR unicode): Host (IP or Hostname) to connect and send to.
        dst_port (int): TCP port to connect to.
        connect_timeout_seconds (int, optional): Connection timeout in seconds.
        broker_endpoint_name (str OR unicode, optional): Name used when connecting to Broker listener. Default is
            "TaniumDataSender". This endpoint name may not be used, and could be for internal reference.
        max_log_lines_per_send (int, optional): Sets a maximum number of rows to send. Data is flattened such that for each
            multi-line answer from each sensor in any row generates a new line. The default is 10000, which can easily
            but surpassed at scale. Set to 0 for unlimited.

    Raises:
        RunTimeError: If connection to the Broker receiver times out.
    """

    def __init__(self, dst_host, dst_port=9999, connect_timeout_seconds=2, broker_endpoint_name="TaniumQuestionData",
                 max_log_lines_per_send=10000):
        self.dst_host = str(dst_host)
        self.dst_port = dst_port
        self.connect_timeout_seconds = connect_timeout_seconds
        self.broker_name = broker_endpoint_name
        self.epc = pybroker.endpoint(self.broker_name)
        self.ocsq = None
        self._connect_to_dest()
        self._check_messages_ok()
        self.max_log_lines_per_send = max_log_lines_per_send

        # all event names defined in the tanium-question-data bro script must start with this string.
        self.event_name_prefix = 'Tanium::QuestionData_'

    def send_answer_rows(self, question_time, result_set, event_name,
                         topic_name='bro/event/taniumquestiondata', logger=None):
        """Sends question results to the destination via Broker.

        Args:
            question_time (datetime): A datetime timestamp indicating when the question was created.
            result_set (taniumpy.object_types.result_set.ResultSet): A pytan Result Set.
            topic_name (str, optional): A string indicating the topic name. The topic name is specified in the Broker
                enabled bro script, like 'Broker::subscribe_to_events(<your_topic_name>)' The default topic name should
                be kept if using the included bro script unmodified.
            event_name (str): A string indicating the Bro event name. The event name is specified in the
                Broker enabled bro script, like
                    'event Tanium::QuestionData-[headingfromini]('
                The [headingfromini] text is the name of the question ini heading above the question being defined.
                This could be something like question1, or could be as descriptive as you'd like. It is important
                that the bro script has an event defined for this, as well as logging defined for the event, with
                a matching number of columns.
            logger (logging.logger): A python logger instance, if desired. Exceptions while sending rows are
                logged here. This is preferable to throwing the exception, since it would stop all rows. If logger is
                not specified, an exception construction a row or sending a row will cause all subsequent row sends to
                stop, as the exception is raised.
        Raises:
            ValueError: if event name does not start with 'Tanium::QuestionData-'
            RunTimeError: if the returned data does not have any of the necessary column names --
                Computer Name, Tanium Client IP Address, or Last Logged In User
                which are prepended to any question, as the first three columns in that order.
        """
        if not event_name.startswith(self.event_name_prefix):
            raise ValueError('Event name must start with \'{}\', was {}'.format(self.event_name_prefix, event_name))

        columns, rows = flatten.flatten(result_set, header_sort=False)

        if len(rows) > self.max_log_lines_per_send and not self.max_log_lines_per_send == 0:
            lines_err = 'Results for event {} would generate {} individual lines, limit is {}'
            raise RuntimeError(lines_err.format(event_name, len(rows), self.max_log_lines_per_send))

        # all questions submitted have been modified by now such that Computer Name and Tanium Client IP Address
        # were added. If so, pull these values out and send only part of rows and columns. If not, somehow, fake them
        # out and send the full rows and cols.

        question_time_unix = (question_time - datetime(1970, 1, 1)).total_seconds()
        d = pybroker.data
        f = pybroker.field
        required_columns = ['Computer Name', 'Tanium Client IP Address', 'Last Logged In User']
        if not len(columns) >= len(required_columns):
            clm = 'Only {} columns in question results, require at least {}'
            raise RuntimeError(clm.format(len(columns), len(required_columns)))

        first_three_col_names = [columns[0]['name'], columns[1]['name'], columns[2]['name']]
        if not first_three_col_names == required_columns:
            cm = 'First three columns are not {}, {}, {} - got {cols} instead'
            raise RuntimeError(cm.format(*required_columns, cols=first_three_col_names))

        # loop through all rows and send each as a broker message
        for i, row in enumerate(rows):
            hostname = row[0]
            client_ip = row[1]
            last_user = row[2]
            try:
                # construct first part of broker message. All python data types have to be processed by pybroker module.
                message_list = [f(d(str(event_name))),
                                f(d(pybroker.time_point(question_time_unix))),
                                f(d(str(hostname))),
                                f(d(pybroker.address_from_string(str(client_ip)))),
                                f(d(str(last_user)))]
            except RuntimeError as e:
                if logger is not None:
                    logger.warning("Could not transform row into Broker types due to data in the first three columns,"
                                   " exception was {}, row had data {}".format(str(e), row))
                else:
                    raise e
                continue
            # now append to broker message the rest of the column data.
            rest_rows = row[3:]
            broker_message_rest = []
            for row_string in rest_rows:
                # strings are printed escaped. Let's unescape the double backslashes
                broker_message_rest.append(f(d(str(row_string.replace('\\\\', '\\')))))
            try:
                message_list.extend(broker_message_rest)
            except RuntimeError as e:
                if logger is not None:
                    logger.warning("Could not transform row into Broker types due to data after the first three "
                                   "columns, exception was {}, row had data {}".format(str(e), row))
                else:
                    raise e
                continue
            try:
                v = pybroker.vector_of_field
                self.epc.send(topic_name, pybroker.message([d(str(event_name)),
                                                            d(pybroker.record(v(message_list)))]))
            except Exception as e:
                if logger is not None:
                    logger.warning("Could not send row to Broker, "
                                   "despite it conforming to Broker types. Exception was {}.".format(str(e)))
                else:
                    raise e

    def _connect_to_dest(self):
        self.epc.peer(self.dst_host, self.dst_port, 1)
        self.ocsq = self.epc.outgoing_connection_status()
        # do low level io connect with configured second timeout
        res = select([self.ocsq.fd()], [], [], self.connect_timeout_seconds)
        if res == ([], [], []):
            raise RuntimeError('Connection to {}:{} timed out after {} seconds.'.format(
                self.dst_host, self.dst_port, self.connect_timeout_seconds
            ))

    def _check_messages_ok(self):
        # with the low level connection up check to make sure high level works
        msgs = self.ocsq.want_pop()
        for m in msgs:
            if not m.status == pybroker.outgoing_connection_status.tag_established:
                raise RuntimeError('Message indicates tag is not established')
