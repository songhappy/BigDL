#
# Copyright 2016 The BigDL Authors.
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
from py4j.protocol import Py4JError

from bigdl.orca.data.utils import *
from bigdl.orca.data.shard import SparkXShards
from bigdl.orca import OrcaContext
from bigdl.dllib.nncontext import init_nncontext, ZooContext
from bigdl.dllib.utils.common import (get_node_and_core_number,
                                      get_spark_sql_context,
                                      get_spark_context)
from bigdl.dllib.utils import nest
from bigdl.dllib.utils.log4Error import invalidInputError

import numpy as np
import pyspark.sql.functions as F
from pyspark import RDD

from typing import (Union, List, Dict)

from typing import TYPE_CHECKING, Any
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    NoReturn
)

if TYPE_CHECKING:
    from numpy import ndarray
    from pyspark.rdd import PipelinedRDD, RDD


class ImageShards(SparkXShards):

    def __init__(self,
                 rdd: Union["PipelinedRDD", "RDD"],
                 transient: bool=False,
                 class_name: str=None) -> None:
        super(ImageShards, self).__init__(rdd, transient, class_name)


def read_im_file(filepath):
    from PIL import Image
    im = Image.open(filepath)
    return im

def read_im_file_cv(filepath):
    import cv2
    im = cv2.imread(filepath, mode='RGB')
    return im


def read_images(file_path):
    sc = OrcaContext.get_spark_context()
    node_num, core_num = get_node_and_core_number()

    file_url_splits = file_path.split("://")
    prefix = file_url_splits[0]

    file_paths = []
    if isinstance(file_path, list):
        [file_paths.extend(extract_one_path(path, os.environ)) for path in file_path]
    else:
        file_paths = extract_one_path(file_path, os.environ)

    if not file_paths:
        invalidInputError(False,
                          "The file path is invalid or empty, please check your data")

    print(file_paths[0])
    num_files = len(file_paths)

    total_cores = node_num * core_num
    num_partitions = num_files if num_files < total_cores else total_cores
    rdd = sc.parallelize(file_paths, num_partitions)

    def loadImage(iterator):
        images = []
        files = []
        for f in iterator:
            image = read_im_file(f)
            images.append(image)
            files.append(f)
        return [files, images]

    def loadImage1(f):
        image = read_im_file(f)
        return {'file': f, 'x': image}

    im_rdd = rdd.mapPartitions(loadImage)

    im_rdd = rdd.map(loadImage1)

    return ImageShards(im_rdd)







