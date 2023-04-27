## Answering Questions by Meta-Reasoning over Multiple Chains of Thought

[**Multi-Chain Reasoning**](https://arxiv.org/abs/2304.13007) (MCR) allows answering complex by introducing a meta-reasoner which reasons over multiple CoTs. MCR can mainly be useful in answering complex questions in which multiple answering strategies are possible.
### MCR System Overview

![Alt text](images/fig_2.png?raw=true "MCR System Overview")

### Running MCR
If you are interested in running MCR, check out our [**demo notebook**](https://colab.research.google.com/drive/1JMhy7pPQQzq4T3JR0ksatJPQf5sqCS3K?usp=sharing).

### Datasets and evaluation
To evaluate MCR, we provide our [dataset readers](src/dataset_readers) and [evaluators](src/pred_evaluators). Code to run end-to-end experiments be released soon.