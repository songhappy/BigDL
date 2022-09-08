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

from bigdl.dllib.feature.common import *
from bigdl.dllib.utils.log4Error import *


if sys.version >= '3':
    long = int
    unicode = str

class XGBClassifier():
    def __init__(self, params=None):
        super(XGBClassifier, self).__init__()
        bigdl_type = "float"
        self.value = callZooFunc("float", "getXGBClassifier", params)

    def setNthread(self, value: int):
        callZooFunc("float", "setXGBClassifierNthread", self.value, value)

    def setNumRound(self, value: int):
        callZooFunc("float", "setXGBClassifierNumRound", self.value, value)

    def setNumWorkers(self, value: int):
        callZooFunc("float", "setXGBClassifierNumWorkers", self.value, value)

    def fit(self, df):
        model = callZooFunc("float", "fitXGBClassifier", self.value, df)
        xgb_model = XGBClassifierModel(model)
        return xgb_model

    def setMissing(self, value: int):
        return callZooFunc("float", "setXGBClassifierMissing", self.value, value)

    def setMaxDepth(self, value: int):
        return callZooFunc("float", "setXGBClassifierMaxDepth", self.value, value)

    def setEta(self, value: float):
        return callZooFunc("float", "setXGBClassifierEta", self.value, value)

    def setGamma(self, value: int):
        return callZooFunc("float", "setXGBClassifierGamma", self.value, value)

    def setTreeMethod(self, value: str):
        return callZooFunc("float", "setXGBClassifierTreeMethod", self.value, value)

    def setObjective(self, value: str):
        return callZooFunc("float", "setXGBClassifierObjective", self.value, value)

    def setNumClass(self, value: str):
        return callZooFunc("float", "setXGBClassifierNumClass", self.value, value)

    def setFeaturesCol(self, value: str):
        return callZooFunc("float", "setXGBClassifierFeaturesCol", self.value, value)


class XGBClassifierModel:
    '''
    XGBClassifierModel is a trained XGBoost classification model. The prediction column
    will have the prediction results.
    '''

    def __init__(self, jvalue):
        super(XGBClassifierModel, self).__init__()
        invalidInputError(jvalue is not None, "XGBClassifierModel jvalue cannot be None")
        self.value = jvalue

    def setFeaturesCol(self, features):
        callZooFunc("float", "setFeaturesXGBClassifierModel", self.value, features)

    def setPredictionCol(self, prediction):
        callZooFunc("float", "setPredictionXGBClassifierModel", self.value, prediction)

    def setInferBatchSize(self, batch_size):
        callZooFunc("float", "setInferBatchSizeXGBClassifierModel", self.value, batch_size)

    def transform(self, dataset):
        df = callZooFunc("float", "transformXGBClassifierModel", self.value, dataset)
        return df

    def saveModel(self, path):
        callZooFunc("float", "saveXGBClassifierModel", self.value, path)

    @staticmethod
    def loadModel(path, numClasses):
        """
        load a pretrained XGBoostClassificationModel
        :param path: pretrained model path
        :param numClasses: number of classes for classification
        """
        jvalue = callZooFunc("float", "loadXGBClassifierModel", path, numClasses)
        return XGBClassifierModel(jvalue=jvalue)


class XGBRegressor():
    def __init__(self):
        super(XGBRegressor, self).__init__()
        bigdl_type = "float"
        self.value = callZooFunc("float", "getXGBRegressor")

    def setNthread(self, value: int):
        callZooFunc("float", "setXGBRegressorNthread", self.value, value)

    def setNumRound(self, value: int):
        callZooFunc("float", "setXGBRegressorNumRound", self.value, value)

    def setNumWorkers(self, value: int):
        callZooFunc("float", "setXGBRegressorNumWorkers", self.value, value)

    def fit(self, df):
        model = callZooFunc("float", "fitXGBRegressor", self.value, df)
        return XGBRegressorModel(model)



class XGBRegressorModel:
    def __init__(self, jvalue):
        super(XGBRegressorModel, self).__init__()
        invalidInputError(jvalue is not None, "XGBRegressorModel jvalue cannot be None")
        self.value = jvalue

    def setFeaturesCol(self, features):
        callZooFunc("float", "setFeaturesXGBRegressorModel", self.value, features)

    def setPredictionCol(self, prediction):
        callZooFunc("float", "setPredictionXGBRegressorModel", self.value, prediction)

    def setInferBatchSize(self, value: int):
        callZooFunc("float", "setInferBatchSizeXGBRegressorModel", self.value, value)

    def transform(self, dataset):
        df = callZooFunc("float", "transformXGBRegressorModel", self.value, dataset)
        return df

    def save(self, path):
        print("start saving in python side")
        callZooFunc("float", "saveXGBRegressorModel", self.value, path)

    @staticmethod
    def load(path):
        jvalue = callZooFunc("float", "loadXGBRegressorModel", path)
        return XGBRegressorModel(jvalue=jvalue)

class LightGBMClassifier():
    def __init__(self):
        super(LightGBMClassifier, self).__init__()
        bigdl_type = "float"
        self.value = callZooFunc("float", "getLightGBMClassifier")

    def setFeaturesCol(self, value: str):
        return callZooFunc("float", "setLGBMClassifierFeaturesCol", self.value, value)

    def setLabelCol(self, value: str):
        callZooFunc("float", "setLGBMClassifierLabelCol", self.value, value)

    def setBoostType(self, value: int):
        callZooFunc("float", "setLGBMClassifierBoostType", self.value, value)

    def fit(self, df):
        model = callZooFunc("float", "fitLGBMClassifier", self.value, df)
        model = LightGBMClassifierModel(model)
        return model

    def setMaxDepth(self, value: int):
        return callZooFunc("float", "setLGBMClassifierMaxDepth", self.value, value)

    def setObjective(self, value: str):
        return callZooFunc("float", "setLGBMClassifierObjective", self.value, value)

    def setLearningRate(self, value: str):
        return callZooFunc("float", "setLGBMClassifierLearningRate", self.value, value)

    def setNumIterations(self, value: int):
        return callZooFunc("float", "setLGBMClassifierNumIterations", self.value, value)

class LightGBMClassifierModel:
    """
    LightGBMClassifierModel is a trained LightGBMClassification model. The prediction column
    will have the prediction results.
    """

    def __init__(self, jvalue):
        super(LightGBMClassifierModel, self).__init__()
        invalidInputError(jvalue is not None, "LightGBMClassifierModel jvalue cannot be None")
        self.value = jvalue

    def setFeaturesCol(self, features):
        callZooFunc("float", "setFeaturesLGBMClassifierModel", self.value, features)

    def setPredictionCol(self, prediction):
        callZooFunc("float", "setPredictionLGBMClassifierModel", self.value, prediction)

    def transform(self, dataset):
        df = callZooFunc("float", "transformLGBMClassifierModel", self.value, dataset)
        return df

    def saveModel(self, path):
        callZooFunc("float", "saveLGBMClassifierModel", self.value, path)

    @staticmethod
    def loadModel(path):
        """
        load a pretrained LightGBMClassificationModel
        :param path: pretrained model path
        """
        jvalue = callZooFunc("float", "loadLGBMClassifierModel", path)
        return LightGBMClassifierModel(jvalue=jvalue)

class LightGBMRegressor():
    def __init__(self):
        super(LightGBMRegressor, self).__init__()
        bigdl_type = "float"
        self.value = callZooFunc("float", "getLightGBMRegressor")

    def setFeaturesCol(self, value: str):
        return callZooFunc("float", "setLGBMRegressorFeaturesCol", self.value, value)

    def setLabelCol(self, value: str):
        callZooFunc("float", "setLGBMRegressorLabelCol", self.value, value)

    def setBoostType(self, value: int):
        callZooFunc("float", "setLGBMRegressorBoostType", self.value, value)

    def fit(self, df):
        model = callZooFunc("float", "fitLGBMRegressor", self.value, df)
        model = LightGBMClassifierModel(model)
        return model

    def setMaxDepth(self, value: int):
        return callZooFunc("float", "setLGBMRegressorMaxDepth", self.value, value)

    def setObjective(self, value: str):
        return callZooFunc("float", "setLGBMRegressorObjective", self.value, value)

    def setLearningRate(self, value: str):
        return callZooFunc("float", "setLGBMRegressorLearningRate", self.value, value)

    def setNumIterations(self, value: int):
        return callZooFunc("float", "setLGBMRegressorNumIterations", self.value, value)

class LightGBMRegressorModel:
    """
    LightGBMRegressorModel is a trained LightGBMRegression model. The prediction column
    will have the prediction results.
    """

    def __init__(self, jvalue):
        super(LightGBMRegressorModel, self).__init__()
        invalidInputError(jvalue is not None, "LightGBMRegressorModel jvalue cannot be None")
        self.value = jvalue

    def setFeaturesCol(self, features):
        callZooFunc("float", "setFeaturesLGBMRegressorModel", self.value, features)

    def setPredictionCol(self, prediction):
        callZooFunc("float", "setPredictionLGBMRegressorModel", self.value, prediction)

    def transform(self, dataset):
        df = callZooFunc("float", "transformLGBMRegressorModel", self.value, dataset)
        return df

    def saveModel(self, path):
        callZooFunc("float", "saveLGBMRegressorModel", self.value, path)

    @staticmethod
    def loadModel(path):
        """
        load a pretrained LightGBMRegressorModel
        :param path: pretrained model path
        """
        jvalue = callZooFunc("float", "loadLGBMRegressorModel", path)
        return LightGBMClassifierModel(jvalue=jvalue)