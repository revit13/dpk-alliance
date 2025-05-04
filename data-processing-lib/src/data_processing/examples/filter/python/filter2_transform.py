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

import argparse
import ast
import json
import pandas as pd
from typing import Dict
import duckdb
import pyarrow as pa
import os
import string
from data_processing.data_access import DataAccess
from data_processing.transform import AbstractTableTransform, TransformConfiguration
from data_processing.utils import CLIArgumentProvider, TransformUtils, get_logger
from .filter_transform import FilterTransform

logger = get_logger(__name__)

short_name = "1filter"
cli_prefix = short_name + "_"

filter_criteria_key = "criteria_list"
""" AST Key holds the list of filter criteria (in SQL WHERE clause format)"""
filter_logical_operator_key = "logical_operator"
""" Key holds the logical operator that joins filter criteria (AND or OR)"""
filter_columns_to_drop_key = "columns_to_drop"
""" AST Key holds the list of columns to drop after filtering"""
filter_input_arrow_folder_key = "input_arrow_folder"
filter_output_arrow_folder_key = "output_arrow_folder"
""" Additional AST Key to hold input and output folders to arrow and meta files"""
filter_doc_id_column_name_key = "doc_id_column_name"

filter_criteria_cli_param = f"{cli_prefix}{filter_criteria_key}"
""" AST Key holds the list of filter criteria (in SQL WHERE clause format)"""
filter_logical_operator_cli_param = f"{cli_prefix}{filter_logical_operator_key}"
""" Key holds the logical operator that joins filter criteria (AND or OR)"""
filter_columns_to_drop_cli_param = f"{cli_prefix}{filter_columns_to_drop_key}"
""" AST Key holds the list of columns to drop after filtering"""
filter_input_arrow_folder_cli_param = f"{cli_prefix}{filter_input_arrow_folder_key}"
filter_output_arrow_folder_cli_param = f"{cli_prefix}{filter_output_arrow_folder_key}"
""" Additional AST Keys to hold input and output paths to the arrow and meta files"""
filter_doc_id_column_name_cli_param = f"{cli_prefix}{filter_doc_id_column_name_key}"

captured_arg_keys = [filter_criteria_key,
                     filter_columns_to_drop_key,
                     filter_input_arrow_folder_key,
                     filter_output_arrow_folder_key,
                     filter_doc_id_column_name_key]
""" The set of keys captured from the command line """

# defaults
filter_criteria_default = ast.literal_eval("[]")
""" The default list of filter criteria (in SQL WHERE clause format)"""
filter_logical_operator_default = "AND"
filter_columns_to_drop_default = ast.literal_eval("[]")
""" The default list of columns to drop"""
filter_doc_id_column_name_default = "id"


class Filter2TransformConfiguration(TransformConfiguration):
    """
    Provides support for configuring and using the associated Transform class include
    configuration with CLI args and combining of metadata.
    """

    def __init__(self):
        super().__init__(
            name=short_name,
            transform_class=FilterTransform,
        )

    def add_input_params(self, parser: argparse.ArgumentParser) -> None:
        """
        Add Transform-specific arguments to the given parser.
        This will be included in a dictionary used to initialize the FilterTransform.
        By convention a common prefix should be used for all mutator-specific CLI args
        (e.g, noop_, pii_, etc.)
        """

        sample_sql = [
            "docq_total_words > 100 AND docq_total_words < 200",
            "docq_perplex_score < 230",
            "date_acquired BETWEEN '2023-07-04' AND '2023-07-08'",
            "title LIKE 'https://%%'",
            "document_id IN ('doc-id-1', 'doc-id-2', 'doc-id-3')",
        ]
        columns_to_drop_example = ["column1", "column2"]

        parser.add_argument(
            f"--{filter_criteria_cli_param}",
            type=ast.literal_eval,
            required=True,
            default=ast.literal_eval("[]"),
            help=f"list of filter criteria (in SQL WHERE clause format), for example: {json.dumps(sample_sql, indent=2, default=str)}",
        )
        parser.add_argument(
            f"--{filter_columns_to_drop_cli_param}",
            type=ast.literal_eval,
            required=False,
            default=ast.literal_eval("[]"),
            help=f"list of columns to drop after filtering, for example: {json.dumps(columns_to_drop_example)}",
        )
        parser.add_argument(
            f"--{filter_logical_operator_cli_param}",
            type=str,
            required=False,
            default="AND",
            choices=["AND", "OR"],
            help="logical operator (AND or OR) that joins filter criteria",
        )
        parser.add_argument(
            f"--{filter_input_arrow_folder_cli_param}",
            type=str,
            required=False,
            default="",
            help="the input path to the .arrow files"
        )
        parser.add_argument(
            f"--{filter_output_arrow_folder_cli_param}",
            type=str,
            required=False,
            default="",
            help="the output path to the .arrow files"
        )
        parser.add_argument(
            f"--{filter_doc_id_column_name_cli_param}",
            type=str,
            required=False,
            default="id",
            help="the unique doc_id column name"
        )

    def apply_input_params(self, args: argparse.Namespace) -> bool:
        """
        Validate and apply the arguments that have been parsed
        :param args: user defined arguments.
        :return: True, if validate pass or False otherwise
        """
        # Capture the args that are specific to this transform
        captured = CLIArgumentProvider.capture_parameters(args, cli_prefix, False)
        self.params = self.params | captured
        logger.info(f"filter 2 parameters are : {self.params}")
        return True