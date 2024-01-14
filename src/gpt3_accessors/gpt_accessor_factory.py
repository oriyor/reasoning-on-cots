from typing import Dict, Type

from src.common.abstract_factory import AbstractFactory
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_base import GptAccessor
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_simple import GptAccessorSimple
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_simple_retrobust import GptAccessorSimpleRetrobust
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_with_retrieval import (
    GptAccessorWithRetrieval,
)
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_with_retrieval_context_first import (
    GptAccessorWithRetrievalContextFirst,
)
from src.gpt3_accessors.gpt3_accessors.gpt_accessor_with_retriever_context_first_retrobust import (
    GptAccessorWithRetrievalContextFirstRetrobust,
)


class GptAccessorFactory(AbstractFactory):
    """ """

    def get_instance_name_to_class_dict(self) -> Dict[str, Type[GptAccessor]]:
        return {
            "gpt_accessor_simple": GptAccessorSimple,
            "gpt_accessor_with_retrieval": GptAccessorWithRetrieval,
            "gpt_accessor_with_retrieval_context_first": GptAccessorWithRetrievalContextFirst,
            "gpt_accessor_simple_retrobust": GptAccessorSimpleRetrobust,
            "gpt_accessor_with_retrieval_context_first_retrobust": GptAccessorWithRetrievalContextFirstRetrobust,
        }
