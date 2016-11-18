
###############################################################################
# WARNING BROKER IS BEING REWRITTEN THIS SENDER MAY NOT WORK AFTER VERSION 0.6
#   This code should be used as a jump point to feed data from pytan to a bro
# box.
###############################################################################

import pybroker  # Requires broker python bindings compiled.
from select import select


class TaniumBrokerSender(object):
    """Creates a connection via Broker API and sends a message.

    Args:
        dst_host (str): Host (IP or Hostname) to connect and send to.
        dst_port (int): TCP port to connect to.
        connect_timeout_seconds (int): Connection timeout in seconds.

    Raises:
        RunTimeError: If connection to the Broker receiver times out.
    """
    def __init__(self, dst_host, dst_port=9999, connect_timeout_seconds=2, broker_name="TaniumDataSender"):
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.connect_timeout_seconds = connect_timeout_seconds
        self.broker_name = broker_name
        self.epc = pybroker.endpoint(self.broker_name)
        self.ocsq = self.epc.outgoing_connection_status()
        self._connect_to_dest()
        self._check_messages_ok()

    def send_message(self, string_message, topic_name='taniumSensorResults'):
        """Sends a string message to the destination via Broker.

        Args:
            string_message (str): A string to send to the destination.
            topic_name (str, optional): A string indicating the topic name
        """
        m = pybroker.message([pybroker.data(string_message)])
        # Send works as a key-value pair. The key is called a "topic". In this
        # example our topic is taniumSensorResults but this could be a more specific
        # name if needed
        self.epc.send(topic_name, m)

    def _connect_to_dest(self):
        self.epc.peer(self.dst_host, self.dst_port, 1)
        # do low level io connect with configured second timeout
        res = select([self.ocsq.fd()], [], [], self.connect_timeout_seconds)
        if res == ([],[],[]):
            raise RuntimeError('Connection to {}:{} timed out after {} seconds.'.format(
                self.dst_host, self.dst_port, self.connect_timeout_seconds
            ))

    def _check_messages_ok(self):
        # with the low level connection up check to make sure high level works
        msgs = self.ocsq.want_pop()
        for m in msgs:
            if not m.status == pybroker.outgoing_connection_status.tag_established:
                raise RuntimeError('Message indicates tag is not established')

