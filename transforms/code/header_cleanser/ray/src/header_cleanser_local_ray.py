# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import os
import sys

from data_processing.utils import ParamsUtils
from data_processing_ray.runtime.ray import RayTransformLauncher
from header_cleanser_transform import (
    column_cli_params,
    license_cli_params,
    copyright_cli_params,
)
from header_cleanser_transform_ray import HeaderCleanserRayTransformConfiguration


# create parameters
input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data/input"))
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
local_conf = {
    "input_folder": input_folder,
    "output_folder": output_folder,
}

header_cleanser_params = {
    column_cli_params: 'contents',
    license_cli_params: True,
    copyright_cli_params: True,
}

worker_options = {"num_cpus": 0.8}
code_location = {"github": "github", "commit_hash": "12345", "path": "path"}
launcher_params = {
    # where to run
    "run_locally": True,
    # Data access. Only required parameters are specified
    "data_local_config": ParamsUtils.convert_to_ast(local_conf),
    # orchestrator
    "runtime_worker_options": ParamsUtils.convert_to_ast(worker_options),
    "runtime_num_workers": 3,
    "runtime_pipeline_id": "pipeline_id",
    "runtime_job_id": "job_id",
    "runtime_creation_delay": 0,
    "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
}

# launch
if __name__ == "__main__":
    # Run the transform inside Ray
    # Create the CLI args as will be parsed by the launcher
    sys.argv = ParamsUtils.dict_to_req(launcher_params | header_cleanser_params)
    # Create the longer to launch with the blocklist transform.
    launcher = RayTransformLauncher(HeaderCleanserRayTransformConfiguration())
    # Launch the ray actor(s) to process the input
    launcher.launch()
