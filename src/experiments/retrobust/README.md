# Running RetRobust Experiments
The [reasoning-on-cots](https://github.com/oriyor/reasoning-on-cots) experiments framework also supports running [RetRobust](https://github.com/oriyor/ret-robust) experiments.

## Preliminaries
Before running the experiment, you will need to set your [FastChat](https://github.com/lm-sys/FastChat) inference endpoints and API keys (when necessary).
### Starting a FastChat server:
To run these experiments, you will need an up-and-running [FastChat](https://github.com/lm-sys/FastChat) server with the relevant LLM. To set up the FastChat server:
1. Set up the controller:
```python3 -m fastchat.serve.controller```
2. Set up the worker with the model you want to run, e.g.: ```python3 -m fastchat.serve.model_worker --model-path meta-llama/Llama-2-13b-hf```
3. Set up the OpenAI inference endpoints: ```python3 -m fastchat.serve.openai_api_server```
4. Make sure the `decomposition.fastchat_url` and `decomposition.fastchat_model` fields in the config point to the relevant url (hosting hte local api server) and model
5. **Important comment**: FastChat adds default messages by default, which are not needed when using our prompts. System messages can be easily removed manually, as shown [here](https://github.com/lm-sys/FastChat/commit/ae9defcb19dd673da3b93ac98e83222f55f649d1). Alternatively, you can use our [forked version of FastChat](https://github.com/oriyor/FastChat) (keep in mind that this is an old version and not all models will be supported). 

### Using SerpAPI and OpenAI
To use SerpAPI and OpenAI, simply set the `SERP_API_KEY` or `OPENAI_KEY` environment variables.

### Using cached retrieval results:
We are also sharing our cached retrieval results for SerpAPI and ColBERT from all out experiments. To use these cached results:
1. Download the retrieval results for [Serp](https://docs.google.com/uc?export=download&id=1SmheDTsKaMTZPZ5ZPQ48Sa4VnoJvcIXi
)/[ColBERT](https://docs.google.com/uc?export=download&id=1ftjv3qW9kV0npW_j68cIZV-CiFGRdfwY).
2. Unzip the folder.
3. Make sure the `decomposition.main_retriever_dir` field in the config is pointing to the unzipped folder.

### Configuring an experiment 
RetRobust experiments require configuring the following fields:
* `settings`: this is the retrieval setting that will be examined. Setting ["reg", "random", "@10"] will run all three retrieval settings. To run a single setting, use the `randomize_retrieval` and `retrieve_at_10` fields.
* `main_retriever_dir`: this is the directory from which cached retrieval results will be read. 
* `run_output_dir`: this is the directory to which retrieval results will be cached (in addition to the `main_retriever_dir`). This repository will be used to read retrieval results when randomizing retrieval.
* The rest of the settings (including the retriever, inference endpoint, and model) are similar to the [reasoning-on-cots](https://github.com/oriyor/reasoning-on-cots) project. For example RetRobust config files, see `src/config/retrobust`.

## Running an experiment
Once your FastChat server is up-and-running, you are good to go. Simply:
1. Set up your config (e.g., `retrobust/nq/with_retrieval_top_1.json`). This will determine the input data, inference model, retrieval model, and evaluation. 
2. Run your experiment:  ```python src/experiments/retrobust/run.py --config_path src/config/retrobust/nq/with_retrieval_top_1.json```
