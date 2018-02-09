/*
 * Copyright 2016 The BigDL Authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.intel.analytics.bigdl.nn.keras

import com.intel.analytics.bigdl.nn.abstractnn.{AbstractModule, TensorModule}
import com.intel.analytics.bigdl.optim.Regularizer
import com.intel.analytics.bigdl.tensor.Tensor
import com.intel.analytics.bigdl.tensor.TensorNumericMath.TensorNumeric
import com.intel.analytics.bigdl.utils.Shape

import scala.reflect.ClassTag

/**
 * Long Short Term Memory unit architecture.
 * The input of this layer should be 3D, i.e. (batch, time steps, input dim).
 *
 * When you use this layer as the first layer of a model, you need to provide the argument
 * inputShape (a Single Shape, does not include the batch dimension).
 *
 * @param outputDim Hidden unit size. Dimension of internal projections and final output.
 * @param activation Activation function to use.
 *                   You can also pass in corresponding string representations such as 'relu'
 *                   or 'sigmoid', etc. for simple activations in the factory method.
 *                   Default is 'tanh'.
 * @param innerActivation Activation function for inner cells.
 *                        You can also pass in corresponding string representations such as 'relu'
 *                        or 'sigmoid', etc. for simple activations in the factory method.
 *                        Default is 'hard_sigmoid'.
 * @param returnSequences Whether to return the full sequence or only return the last output,
 *                        in the output sequence. Default is false.
 * @param goBackwards Whether the input sequence will be processed backwards. Default is false.
 * @param wRegularizer An instance of [[Regularizer]], (eg. L1 or L2 regularization),
 *                     applied to the input weights matrices. Default is null.
 * @param uRegularizer An instance of [[Regularizer]], applied the recurrent weights matrices.
 *                     Default is null.
 * @param bRegularizer An instance of [[Regularizer]], applied to the bias. Default is null.
 * @tparam T Numeric type of parameter(e.g. weight, bias). Only support float/double now.
 */
class LSTM[T: ClassTag](
   outputDim: Int,
   val activation: AbstractModule[Tensor[T], Tensor[T], T] = null,
   val innerActivation: AbstractModule[Tensor[T], Tensor[T], T] = null,
   returnSequences: Boolean = false,
   goBackwards: Boolean = false,
   var wRegularizer: Regularizer[T] = null,
   var uRegularizer: Regularizer[T] = null,
   var bRegularizer: Regularizer[T] = null,
   inputShape: Shape = null)(implicit ev: TensorNumeric[T])
  extends Recurrent[T](outputDim, returnSequences, goBackwards, inputShape) {

  override def doBuild(inputShape: Shape): AbstractModule[Tensor[T], Tensor[T], T] = {
    val input = inputShape.toSingle().toArray
    val layer = com.intel.analytics.bigdl.nn.LSTM[T](
      inputSize = input(2),
      hiddenSize = outputDim,
      activation = activation.asInstanceOf[TensorModule[T]],
      innerActivation = innerActivation.asInstanceOf[TensorModule[T]],
      wRegularizer = wRegularizer,
      uRegularizer = uRegularizer,
      bRegularizer = bRegularizer)
    super.processParameters(layer)
  }
}

object LSTM {
  def apply[@specialized(Float, Double) T: ClassTag](
    outputDim: Int,
    activation: String = "tanh",
    innerActivation: String = "hard_sigmoid",
    returnSequences: Boolean = false,
    goBackwards: Boolean = false,
    wRegularizer: Regularizer[T] = null,
    uRegularizer: Regularizer[T] = null,
    bRegularizer: Regularizer[T] = null,
    inputShape: Shape = null)(implicit ev: TensorNumeric[T]) : LSTM[T] = {
    new LSTM(outputDim, KerasUtils.getActivation(activation),
      KerasUtils.getActivation(innerActivation), returnSequences,
      goBackwards, wRegularizer, uRegularizer, bRegularizer, inputShape)
  }
}
