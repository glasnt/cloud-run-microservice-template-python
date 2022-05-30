# Copyright 2021 Google LLC
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

import json
import logging
import signal
import sys
from types import FrameType

import google.cloud.logging
from flask import Flask

# Setup google-cloud-logging
client = google.cloud.logging.Client()
client.setup_logging()

app = Flask(__name__)


@app.route("/")
def hello() -> str:
    # Use basic logging with custom fields
    # https://googleapis.dev/python/logging/latest/UPGRADING.html#full-json-log-support-in-standard-library-integration-316-339-447
    extra_data = dict(logField="custom-entry", arbitraryField="custom-entry")
    logging.info(json.dumps(extra_data))

    # https://cloud.google.com/run/docs/logging#correlate-logs
    logging.info("Child logger with trace Id.")

    return "Hello, World!"


def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logging.info(f"Caught Signal {signal.strsignal(signal_int)}")

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
