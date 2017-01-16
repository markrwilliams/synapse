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

from mock import Mock

from synapse.app.media_repository import MediaRepositoryServer

from tests import unittest

from .common import assert_replicate_logs_failure


class MediaRepositoryServerTestCase(unittest.TestCase):
    """
    Tests for :class:`synapse.app.appservice.MediaRepositoryServer`.
    """

    def setUp(self):
        self.config = Mock()
        self.version_string = "Synapse/Test"
        self.server = MediaRepositoryServer(
            "test",
            config=self.config,
            version_string=self.version_string)

    def test_replicate_logs_failure(self):
        assert_replicate_logs_failure(self, self.server)
