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
# ===========================================================================
#
# This file is adapted from
# https://github.com/mit-han-lab/streaming-llm/blob/main/examples/run_streaming_llama.py
# which is licensed under the MIT license:
#
# MIT License
#
# Copyright (c) 2023 MIT HAN Lab
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import warnings
import torch
import argparse
import os
#from transformers.utils import is_torch_xpu_available
import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
stream_llm_src = CURRENT_DIR.replace("GPU", "CPU") + "/streaming_llm/"
sys.path.append(stream_llm_src)
from utils import load, download_url, load_jsonl
from enable_streaming_llm import enable_streaming_llm
warnings.filterwarnings("ignore")


@torch.no_grad()
def greedy_generate(model, tokenizer, input_ids, past_key_values, max_gen_len):
    import time 
    first_start=time.time()
    outputs = model(
        input_ids=input_ids,
        past_key_values=past_key_values,
        use_cache=True,
    )
    first_end=time.time()
    first_time=first_end-first_start
    print("first time:", first_time)    
    past_key_values = outputs.past_key_values
    pred_token_idx = outputs.logits[:, -1, :].argmax(dim=-1).unsqueeze(1)
    generated_ids = [pred_token_idx.item()]
    pos = 0
    next_times= []
    for _ in range(max_gen_len - 1):
        next_start=time.time()
        outputs = model(
            input_ids=pred_token_idx,
            past_key_values=past_key_values,
            use_cache=True,
        )
        next_end=time.time()
        next_times.append(next_end-next_start)
        past_key_values = outputs.past_key_values
        pred_token_idx = outputs.logits[:, -1, :].argmax(dim=-1).unsqueeze(1)
        generated_ids.append(pred_token_idx.item())
        generated_text = (
            tokenizer.decode(
                generated_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
                spaces_between_special_tokens=False,
            )
            .strip()
            .split(" ")
        )

        now = len(generated_text) - 1
        if now > pos:
            print(" ".join(generated_text[pos:now]), end=" ", flush=True)
            pos = now

        # if pred_token_idx == tokenizer.eos_token_id:
        #     break
    
    next_time=sum(next_times)/len(next_times)
    print("\n","next time:", next_time)    

    print(" ".join(generated_text[pos:]), flush=True)
    return past_key_values, first_time, next_time


@torch.no_grad()
def streaming_inference(model, tokenizer, prompts, kv_cache=None, max_gen_len=32):
    past_key_values = None
    import time

    first_times = []
    next_times = []
    for idx, prompt in enumerate(prompts):
        print("***************************idx=", idx)
        print("prompt:", prompt)
        prompt = "USER: " + prompt[:] + "\n\nASSISTANT: "
        print("\n" + prompt, end="")
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        input_ids = input_ids.to(model.device)
        seq_len = input_ids.shape[1]
        print("sequence length:", seq_len)

        if kv_cache is not None:
            space_needed = seq_len + max_gen_len
            past_key_values = kv_cache.evict_for_space(past_key_values, space_needed)

        past_key_values, first_time, next_time = greedy_generate(
            model, tokenizer, input_ids, past_key_values, max_gen_len=max_gen_len
        )
        print("past_key_values[0].shape", past_key_values[0][0].shape)
        print("past_key_values[1].shape", past_key_values[1][0].shape)

        if idx > 1:
            first_times.append(first_time)
            next_times.append(next_time)
    import math
    print("first_times:", sum(first_times)/len(first_times)) 
    print("next_times:", sum(next_times)/len(next_times))
        

def main(args):
    model, tokenizer = load(args.repo_id_or_model_path)
    #device = 'xpu' if is_torch_xpu_available() else 'cpu'
    device='xpu'
    model = model.to(device)
    test_filepath = os.path.join(args.data_root, "mt_bench.jsonl")
    print(f"Loading data from {test_filepath} ...")

    if not os.path.exists(test_filepath):
        download_url(
            "https://raw.githubusercontent.com/lm-sys/FastChat/main/fastchat/llm_judge/data/mt_bench/question.jsonl",
            args.data_root,
        )
        os.rename(os.path.join(args.data_root, "question.jsonl"), test_filepath)

    list_data = load_jsonl(test_filepath)
    
    prompts = []
    for sample in list_data[:]:
        prompts += sample["turns"]
        print(sample["turns"])
    print("------------------------------------------prompts")
    print(len(prompts))
    for _ in prompts:
        print(_)
    if args.enable_streaming:
        kv_cache = enable_streaming_llm(
            model, start_size=args.start_size, recent_size=args.recent_size
        )
    else:
        kv_cache = None

    streaming_inference(
        model,
        tokenizer,
        prompts,
        kv_cache,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-id-or-model-path", type=str, default="meta-llama/Llama-2-7b-chat-hf"
    )
    parser.add_argument("--data-root", type=str, default="data/")
    parser.add_argument("--enable-streaming", action="store_true")
    parser.add_argument("--start-size", type=int, default=4)
    parser.add_argument("--recent-size", type=int, default=500)
    args = parser.parse_args()

    main(args)
