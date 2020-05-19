#!/usr/bin/env python

# Copyright 2018 Google LLC.
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

import os
import uuid

from google.cloud import pubsub_v1
from google.cloud import resource_manager

import quickstart_createfeed
import quickstart_deletefeed

PROJECT = os.environ['GCLOUD_PROJECT']
ASSET_NAME = 'assets-{}'.format(uuid.uuid4().hex)
FEED_ID = 'feed-{}'.format(uuid.uuid4().hex)
TOPIC = 'topic-{}'.format(uuid.uuid4().hex)


def test_delete_feed(capsys):
    client = resource_manager.Client()
    project_number = client.fetch_project(PROJECT).number
    # First create the feed, which will be deleted later
    full_topic_name = "projects/{}/topics/{}".format(PROJECT, TOPIC)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, TOPIC)
    publisher.create_topic(topic_path)
    quickstart_createfeed.create_feed(
        PROJECT, FEED_ID, [ASSET_NAME, ], full_topic_name)

    feed_name = "projects/{}/feeds/{}".format(project_number, FEED_ID)
    quickstart_deletefeed.delete_feed(feed_name)

    out, _ = capsys.readouterr()
    assert "deleted_feed" in out
    publisher.delete_topic(topic_path)
