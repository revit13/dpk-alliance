import os
import sys

from data_processing.utils import ParamsUtils
from data_processing.runtime.spark import SparkTransformLauncher
from pipeline_transform_demo import PipelineForkSparkTransformConfiguration

# create parameters
input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "input"))
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "output"))

bad_word_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../doc_quality", "ldnoobw"))
local_conf = {
    "input_folder": input_folder,
    "output_folder": output_folder,
}

local_conf_input = {
    "input_folder": input_folder,
}
local_conf_output = {
    "output_folder": output_folder,
}
worker_options = {"num_cpus": 0.8}
filter_en_criteria = [
    "lang = \'en\' AND contents != \'\'"
]
#filter_logical_operator = "AND"
filter_en_params = {
    "filter_criteria_list": filter_en_criteria,
}

filter_jp_criteria = [
    "lang = \'ja\' AND contents != \'\'"
]
#filter_logical_operator = "AND"
filter_jp_params = {
    "filter_1__criteria_list": filter_jp_criteria,
}

docq_ja = {
    "docq_1_bad_word_filepath": bad_word_filepath+ "/ja",
    "docq_1_text_lang": "ja"
}
params = {
    "data_local_config": ParamsUtils.convert_to_ast(local_conf),
    "runtime_parallelization": 1,

    "lang_id_model_credential": os.getenv('HF_TOKEN'),
    "lang_id_model_url": "facebook/fasttext-language-identification",
    "lang_id_model_kind": "fasttext",

    "docq_bad_word_filepath": bad_word_filepath + "/en",

}

# create launcher
sys.argv = ParamsUtils.dict_to_req(d=params | filter_en_params | filter_jp_params | docq_ja)
launcher = SparkTransformLauncher(runtime_config=PipelineForkSparkTransformConfiguration())



# launch
launcher.launch()
