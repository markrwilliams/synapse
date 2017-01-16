# -*- coding: utf-8 -*-
# Copyright 2017 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Common test code for :module:`synapse.app.appservice` services.
"""
from mock import Mock, create_autospec

from twisted.internet.task import Clock
from twisted.internet import defer

from synapse.http.client import SimpleHttpClient
from synapse.util import async


class _TestException(Exception):
    """
    An exception for testing error logging.
    """


def assert_replicate_logs_failure(test_case, server):
    """
    Assert that a server's ``replicate`` method logs replication
    failures.

    Args:
        test_case (test.unittest.TestCase): the server class' test case
        server (synapse.server.HomeServer): the server to test
    """
    # ensure synapse.utl.async.sleep doesn't use the reactor
    test_case.patch(async, "reactor", Clock())

    # called by replicate methods, but not used by this test
    test_case.server.get_datastore = create_autospec(
        test_case.server.get_datastore)

    # ensure http_client.get_json fails
    get_json_deferred = defer.fail(_TestException())
    http_client = Mock(spec=SimpleHttpClient)
    http_client.get_json = create_autospec(SimpleHttpClient.get_json,
                                           return_value=get_json_deferred)
    test_case.server.get_simple_http_client = create_autospec(
        test_case.server.get_simple_http_client,
        return_value=http_client,
    )

    # the method under test
    test_case.server.replicate()

    logged_failures = test_case.flushLoggedErrors()
    test_case.assertEqual(len(logged_failures), 1)
    test_case.assertIsInstance(logged_failures[0].value, _TestException)
