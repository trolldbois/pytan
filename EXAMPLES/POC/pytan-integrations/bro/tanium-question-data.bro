###############################################################################
# This is the Tanium Question Data Bro script which is a requirement for Tanium
# data to be sent to a Bro instance via the Broker API.
#
# This requires that Bro be configured with Broker support. Compiling Broker
# itself is a prerequisite. instructions on compiling Broker are here:
#       https://github.com/bro/broker
# Pay particular attention to the prerequisites for compling Broker, and do not
# forget to clone the Bro cmake submodule in the Broker source directory. To do
# this, run
#       git clone https://github.com/bro/cmake
# in the root of the Broker source directory, such that a cmake directory is
# created and filled.
#
# Broker should be compiled on the Bro machine that listens for connections,
# and it is recommended that the Tanium Bro integration python scripts also
# run from.
#
# This Bro script should be placed in your <Bro dir>/share/bro/site directory.
# Once Bro is restarted, netstat should show that Broker is listening for
# connections on the port specified in the file.
#
# If a field is typically modified, a comment # Modify appears either before or
# in-line.
#
# Critically, it is important that each bro script be modified to match the
# pytan_bro.ini file questions. This means knowing the counts of columns
# and names of columns coming from Tanium.
################################################################################

const broker_port: port = 9999/tcp &redef; # Modify: this is the port that the Broker
redef exit_only_after_terminate = T;

## This is the name of the Broker endpoint. It is not strictly necessary to
## match the endpoint name in the Tanium bro integration python script, but for
## consistency, the default value of in the TaniumBrokerSender class is
## TaniumQuestionData
redef Broker::endpoint_name = "TaniumQuestionData";

event bro_init()
    {
     Broker::enable();
     Broker::listen(broker_port, "0.0.0.0");  # Modify: 0.0.0.0 listens on all
     Broker::subscribe_to_events("bro/event/taniumquestiondata");
    }

# ---------- Debug --------- #
# Uncomment this if you want to see that the Tanium Bro Integration script
# successfully connected as a stdout message
#event Broker::incoming_connection_established(peer_name: string)
#    {
#     print "Broker::Connection established to this listening endpoint", peer_name;
#    }

# ---------- Debug --------- #
# Uncomment this if you want to see that the Tanium Bro Integration script
# disconnecting as a stdout message
#event Broker::incoming_connection_broken(peer_name: string)
#    {
#     print "Broker::incoming_connection_broken", peer_name;
#     terminate();
#    }


# defines Tanium as a namespace, and adds log and data format for Tanium messages.
module Tanium;
export
   {
    # Append the value LOG to the Log::ID enumerable.

    redef enum Log::ID += { LOG_question1, LOG_question2 };

    # Define a new type called Tanium::Info.
    type question1: record {
        question_timestamp:     time &log;
        host:                   string &log;
        ip:                     addr &log;
        last_logged_in_user:    string &log;
        model:                  string &log;
        computer_serial_number: string &log;
        };

    type question2: record {
        question_timestamp:     time &log;
        host:                   string &log;
        ip:                     addr &log;
        last_logged_in_user:    string &log;
        path:                   string &log;
        md5_hash:               string &log;
        };

     # This defines the message formats. For each Tanium::QuestionData-x event
     # name, there is a matching record type of columns, and a matching event
     # definition here.
     # The first three fields always exist, as the integration code adds them
     # to your questions, but the rest of the column names must be defined by
     # you. The column names are visible when asking the question in the
     # Tanium console.
     # question_data field consists of columns returned.

     # There is one entry here for each question defined in the pytan_bro.ini
     # file. Keep the default columns for the events up to and including
     # last logged in user, but add additional columns for the data
     # which will all have the type 'string'

     global QuestionData_question1: event(question_timestamp: time, host: string,
                                          ip: addr, last_logged_in_user: string,
                                          model: string,
                                          computer_serial_number: string);

     global QuestionData_question2: event(question_timestamp: time, host: string,
                                          ip: addr, last_logged_in_user: string,
                                          path: string,
                                          md5_hash: string);
   }

# Modify: the log file name is specified as $path here. The default should be
# acceptable, as it matches the integration name. Each question receives its
# own log path, and the name of the stream is LOG_questionx, where questionx is
# the ini file heading in pytan_bro.ini
event bro_init()
    {
     # Create the logging stream for question types
     Log::create_stream(LOG_question1, [$columns=question1, $path="tanium_question_data-question1"]);
     Log::create_stream(LOG_question2, [$columns=question2, $path="tanium_question_data-question2"]);
    }

event Tanium::QuestionData_question1(question_timestamp: time, host: string, ip: addr, last_logged_in_user: string,
                                     model: string,
                                     computer_serial_number: string)
   {
    Log::write( Tanium::LOG_question1, [$question_timestamp=question_timestamp, $host=host, $ip=ip, $last_logged_in_user=last_logged_in_user,
                                        $model=model, $computer_serial_number=computer_serial_number] );

    # Modify: Uncomment in order to see the data on stdout.
    # print "Broker received Tanium Question Data", question_timestamp, host, ip, last_logged_in_user, question_data;
   }

event Tanium::QuestionData_question2(question_timestamp: time, host: string, ip: addr, last_logged_in_user: string,
                                     path: string,
                                     md5_hash: string)
   {
    Log::write( Tanium::LOG_question2, [$question_timestamp=question_timestamp, $host=host, $ip=ip, $last_logged_in_user=last_logged_in_user,
                                        $path=path, $md5_hash=md5_hash] );

    # Modify: Uncomment in order to see the data on stdout.
    # print "Broker received Tanium Question Data", question_timestamp, host, ip, last_logged_in_user, question_data;
   }