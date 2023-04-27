## ⛓️ Answering Questions by Meta-Reasoning over Multiple Chains of Thought

[**Multi-Chain Reasoning**](https://arxiv.org/abs/2304.13007) (MCR) allows answering complex by introducing a meta-reasoner which reasons over multiple CoTs. MCR can mainly be useful in answering complex questions in which multiple answering strategies are possible.
### MCR System Overview

![Alt text](images/overview2.png?raw=true "MCR System Overview")

### 🤖 Running MCR
If you are interested in running MCR, check out our [**demo notebook**](https://colab.research.google.com/drive/1JMhy7pPQQzq4T3JR0ksatJPQf5sqCS3K?usp=sharing).

### ⛰️ Datasets and evaluation
To evaluate MCR, we provide our [dataset readers](src/dataset_readers) and [evaluators](src/pred_evaluators). Code to run end-to-end experiments be released soon.

### ✍ Citation

```
bibtex
@article{yoran-etal-2023-answering,
    title={Answering Questions by Meta-Reasoning over Multiple Chains of Thought}, 
    author={Ori Yoran and Tomer Wolfson and Ben Bogin and Uri Katz and Daniel Deutch and Jonathan Berant},
    year={2023},
    eprint={2304.13007},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
