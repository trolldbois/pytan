#!/usr/bin/env python
import sys
import os
import unittest

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
par_dir = os.path.join(my_dir, os.pardir)
path_adds = [my_dir, par_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.insert(0, aa)

import api

# from taniumpy.object_types.base import BaseType
# from taniumpy.object_types.user_list import UserList
# from taniumpy.object_types.user_role import UserRole


class TestDeserializeUsers(unittest.TestCase):

    USERS_SOAP_RESPONSE = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<soap:Body xmlns:t="urn:TaniumSOAP" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<t:return><command>GetObject</command>
<session>1-198-b4b5cf866668bdef43d83a9b37a48ec4837de1b20c45bd19bc292bb22972207e0b8c107c69078c06b6394103c5482cbe03cfb681c29f22972222059ca1546126</session>
<ID></ID>
<IDType></IDType>
<ContextID></ContextID>
<result_object><users><user><id>1</id>
<name>tanium</name>
<domain></domain>
<group_id>0</group_id>
<roles><role><id>1</id>
<name>Administrator</name>
<description>Administrators can perform all functions in the system, including creating other users, viewing the System Status, changing Global Settings, and creating Computer Groups.</description>
<permissions><permission>admin</permission>
<permission>sensor_read</permission>
<permission>sensor_write</permission>
<permission>question_read</permission>
<permission>question_write</permission>
<permission>action_read</permission>
<permission>action_write</permission>
<permission>action_approval</permission>
<permission>notification_write</permission>
<permission>clients_read</permission>
<permission>question_log_read</permission>
<permission>content_admin</permission>
</permissions>
</role>
</roles>
<permissions><permission>admin</permission>
<permission>sensor_read</permission>
<permission>sensor_write</permission>
<permission>question_read</permission>
<permission>question_write</permission>
<permission>action_read</permission>
<permission>action_write</permission>
<permission>action_approval</permission>
<permission>notification_write</permission>
<permission>clients_read</permission>
<permission>question_log_read</permission>
<permission>content_admin</permission>
</permissions>
<local_admin_flag>1</local_admin_flag>
<last_login>2014-11-06T15:51:47</last_login>
<deleted_flag>0</deleted_flag>
</user>
<user><id>5</id>
<name>QuestionAuthor</name>
<domain></domain>
<group_id>1</group_id>
<roles><role><id>3</id>
<name>Question Author</name>
<description>Question Authors can ask new questions, and save them. They cannot issue actions, or create packages and sensors.</description>
<permissions><permission>sensor_read</permission>
<permission>question_read</permission>
<permission>question_write</permission>
</permissions>
</role>
</roles>
<permissions><permission>sensor_read</permission>
<permission>question_read</permission>
<permission>question_write</permission>
</permissions>
<local_admin_flag>-1</local_admin_flag>
<last_login>2001-01-01T00:00:00</last_login>
<deleted_flag>0</deleted_flag>
<metadata><item><name>TConsole.User.Property.foo</name>
<value>bar</value>
<admin_flag>1</admin_flag>
</item>
</metadata>
</user>
</users>
</result_object>
<ResultXML></ResultXML>
<options><aggregate_over_time_flag></aggregate_over_time_flag>
<cache_expiration></cache_expiration>
<cache_filters></cache_filters>
<cache_id></cache_id>
<cache_sort_fields></cache_sort_fields>
<context_id></context_id>
<filter_not_flag></filter_not_flag>
<filter_string></filter_string>
<flags></flags>
<hide_errors_flag></hide_errors_flag>
<hide_no_results_flag></hide_no_results_flag>
<include_answer_times_flag></include_answer_times_flag>
<include_hashes_flag></include_hashes_flag>
<include_hidden_flag></include_hidden_flag>
<include_user_details></include_user_details>
<json_pretty_print></json_pretty_print>
<most_recent_flag></most_recent_flag>
<pct_done_limit></pct_done_limit>
<recent_result_buckets></recent_result_buckets>
<return_cdata_flag></return_cdata_flag>
<return_lists_flag></return_lists_flag>
<row_count></row_count>
<row_counts_only_flag></row_counts_only_flag>
<row_start></row_start>
<sample_count></sample_count>
<sample_frequency></sample_frequency>
<sample_start></sample_start>
<script_data></script_data>
<sort_order></sort_order>
<suppress_object_list></suppress_object_list>
<suppress_scripts></suppress_scripts>
<use_error_objects></use_error_objects>
<use_json>0</use_json>
<use_user_context_flag></use_user_context_flag>
</options>
</t:return></soap:Body>
</soap:Envelope>
"""

    def test_deserialize_users(self):
        users = api.BaseType.fromSOAPBody(self.USERS_SOAP_RESPONSE)
        self.assertIsInstance(users, api.UserList)
        self.assertEqual(len(users.user), 2)
        self.assertEquals(users.user[0].name, 'tanium')
        self.assertIsInstance(users.user[0].roles.role[0], api.UserRole)
        # validate that list convenience is available on e.g. users, roles
        self.assertEquals(len(users), 2)
        self.assertEquals(users[0].name, 'tanium')
        self.assertIsInstance(users[0].roles[0], api.UserRole)


if __name__ == "__main__":
    unittest.main()
