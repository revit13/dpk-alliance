from data_processing.examples.noop.spark import (
    NOOPSparkTransformConfiguration,
    NOOP1SparkTransformConfiguration,
    NOOP2SparkTransformConfiguration,
    NOOP3SparkTransformConfiguration,
    NOOP4SparkTransformConfiguration,
)
from data_processing.examples.resize.spark import ResizeSparkTransformConfiguration
from data_processing.examples.doc_quality.spark import DocQualitySparkTransformConfiguration, DocQuality2SparkTransformConfiguration
from data_processing.examples.doc_id.spark import DocIDSparkTransformConfiguration
from data_processing.examples.filter.spark import FilterSparkTransformConfiguration, Filter2SparkTransformConfiguration
from data_processing.examples.lang_id.spark import LangIdentificationSparkTransformConfiguration
from data_processing.transform import PipelineTransformConfiguration
from data_processing.transform.spark import SparkPipelineTransform
from data_processing.data_access import DataAccess, DataAccessFactoryBase
from data_processing.transform.spark.transform_runtime import DefaultSparkTransformRuntime
from data_processing.utils import get_logger
from data_processing.runtime.spark import (
    SparkTransformLauncher,
    SparkTransformRuntimeConfiguration,
)

logger = get_logger(__name__)

class PipelineENFlowSparkTransformConfiguration(SparkTransformRuntimeConfiguration):
    def __init__(self):
        """
        Initialization
        """
        super().__init__(
            transform_config=PipelineTransformConfiguration(
                pipeline=[
                    FilterSparkTransformConfiguration(),
                    DocQualitySparkTransformConfiguration(),
                ],
                transform_class=SparkPipelineTransform,
            )
        )

class PipelineJPFlowSparkTransformConfiguration(SparkTransformRuntimeConfiguration):
    def __init__(self):
        """
        Initialization
        """
        super().__init__(
            transform_config=PipelineTransformConfiguration(
                pipeline=[
                    Filter2SparkTransformConfiguration(),
                    DocQuality2SparkTransformConfiguration(),
                ],
                transform_class=SparkPipelineTransform,
            )
        )
class PipelineForkSparkTransformConfiguration(SparkTransformRuntimeConfiguration):
    def __init__(self):
        """
        Initialization
        """
        pipeline_en_flow = PipelineENFlowSparkTransformConfiguration()
        pipeline_jp_flow = PipelineJPFlowSparkTransformConfiguration()
        super().__init__(
            transform_config=PipelineTransformConfiguration(
                pipeline=[
                    LangIdentificationSparkTransformConfiguration(),
                    [
                        pipeline_en_flow,
                        pipeline_jp_flow
                    ],
                ],
                transform_class=SparkPipelineTransform,
            )
        )



if __name__ == "__main__":
    launcher = SparkTransformLauncher(PipelineForkSparkTransformConfiguration())
    logger.info("Launching resize/noop transform")
    launcher.launch()
