import os
import sys

from data_processing.runtime.python import (
    PythonTransformLauncher,
    PythonTransformRuntimeConfiguration,
)
from data_processing.examples.noop.python import (
    NOOPPythonTransformConfiguration,
    NOOP1PythonTransformConfiguration,
)
from data_processing.examples.resize.python import ResizePythonTransformConfiguration, Resize1PythonTransformConfiguration, Resize2PythonTransformConfiguration, Resize3PythonTransformConfiguration
from data_processing.transform import PipelineTransformConfiguration
from data_processing.transform.python import PythonPipelineTransform
from data_processing.utils import get_logger
from data_processing.utils import ParamsUtils


logger = get_logger(__name__)

class PipelineFork2PythonTransformConfiguration(PythonTransformRuntimeConfiguration):
    """
    Implements the PythonTransformConfiguration for NOOP as required by the PythonTransformLauncher.
    NOOP does not use a RayRuntime class so the superclass only needs the base
    python-only configuration.
    """

    def __init__(self):
        """
        Initialization
        """
        super().__init__(
            transform_config=PipelineTransformConfiguration(
                pipeline=[[
                        Resize1PythonTransformConfiguration(),
                        NOOP1PythonTransformConfiguration(),
                    ]
                ],
                transform_class=PythonPipelineTransform,
            )
        )


if __name__ == "__main__":
    launcher = PythonTransformLauncher(PipelineFork2PythonTransformConfiguration())
    # create parameters
    # input_folder = compute_data_location("test-data/resize/input")
    input_folder = "/data/revital/dpk/transforms/universal/resize/spark/test-data/input/"
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
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
        "resize_max_rows_per_table": 250,
        "noop7_sleep_sec": 5,
    }
    sys.argv = ParamsUtils.dict_to_req(d=params)
    logger.info("Launching resize/noop transform")
    launcher.launch()
