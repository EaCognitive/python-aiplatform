"""Tests for Sandbox Snapshot create operation."""

# Copyright 2026 Google LLC
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
#
# pylint: disable=protected-access,bad-continuation,missing-function-docstring,bad-indentation

from tests.unit.vertexai.genai.replays import pytest_helper
from vertexai._genai import types


def test_create_sandbox_snapshot(client):
  # 1. Create an Agent Engine
  agent_engine = client.agent_engines.create()

  # 2. Create a Sandbox
  sandbox_op = client.agent_engines.sandboxes.create(
      name=agent_engine.api_resource.name,
      poll_interval_seconds=1,
      spec={
          "code_execution_environment": {
              "machineConfig": "MACHINE_CONFIG_VCPU4_RAM4GIB"
          }
      },
      config=types.CreateAgentEngineSandboxConfig(
          display_name="test_sandbox", ttl="3600s"
      ),
  )
  sandbox = sandbox_op.response

  # 3. Create a Snapshot
  snapshot = client.agent_engines.sandboxes.snapshots.create(
      name=sandbox.name,
      sandbox_environment_snapshot={},
  )

  assert isinstance(snapshot, types.SandboxEnvironmentSnapshot)


pytestmark = pytest_helper.setup(
    file=__file__,
    globals_for_file=globals(),
    test_method="agent_engines.sandboxes.snapshots.create",
)
