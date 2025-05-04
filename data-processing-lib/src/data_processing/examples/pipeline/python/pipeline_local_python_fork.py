import os
import sys

from data_processing.runtime.python import PythonTransformLauncher
from data_processing.utils import ParamsUtils
from pipeline_transform_fork import PipelineForkPythonTransformConfiguration
from data_processing.data_access import compute_data_location


# create launcher
launcher = PythonTransformLauncher(
    runtime_config=PipelineForkPythonTransformConfiguration()
)
# create parameters
#input_folder = compute_data_location("test-data/resize/input")
input_folder = "/data/revital/dpk/transforms/universal/resize/spark/test-data/input/"

#output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
output_folder = "/data/revital/dpk/transforms/universal/resize/spark/test-data/output/"
local_conf = {
    "input_folder": input_folder,
    "output_folder": output_folder,
}
worker_options = {"num_cpus": 0.8}
params = {
    # Data access. Only required parameters are specified
    "data_local_config": ParamsUtils.convert_to_ast(local_conf),
    # resize configuration
    # "resize_max_mbytes_per_table":  0.02,
    #"resize_max_rows_per_table": 1000,
   # "resize_1max_rows_per_table": 1000,
    #"resize_2max_rows_per_table": 1000,
   # "resize_3max_rows_per_table": 1000,
    "noop1_sleep_sec": 1,
    "noop2_sleep_sec": 2,
    "noop_sleep_sec": 0,
    "noop3_sleep_sec": 3


}
sys.argv = ParamsUtils.dict_to_req(d=params)

# launch
launcher.launch()
