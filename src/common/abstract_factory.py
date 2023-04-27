from abc import ABC
from threading import Lock
from typing import Dict, TypeVar, Generic

from src.common.logger import get_logger

logger = get_logger()

T = TypeVar("T")


class AbstractFactory(ABC, Generic[T]):
    """
    Abstract class to represent a factory.
    The concrete class factory should only implement the method `get_instance_name_to_class_dict`.
    By default, Each instance is kept one time (\singleton), unless one is passing `use_cache=False`.
    """

    def __init__(self):
        self._instances_dict: Dict[str, T] = {}
        self._lock = Lock()

    def get_instance_name_to_class_dict(self) -> Dict[str, T]:
        raise NotImplementedError()

    def get_instance(self, instance_name: str, use_cache: bool = True, *args, **kwargs):
        cleaned_instance_name = instance_name.lower()

        # check if we already created that instance from before and use it
        if cleaned_instance_name in self._instances_dict and use_cache:
            return self._instances_dict[cleaned_instance_name]

        # map from instance name to instance type
        instance_class = self.get_instance_name_to_class_dict().get(
            cleaned_instance_name
        )
        if not instance_class:
            raise ValueError(
                f"{cleaned_instance_name} does not exist. "
                f"Please choose from {self.get_instance_name_to_class_dict().keys()}"
            )

        with self._lock:
            # check again that the instance was not created from other threads
            if cleaned_instance_name in self._instances_dict and use_cache:
                return self._instances_dict[cleaned_instance_name]

            # instantiate the class
            instance = instance_class.create(*args, **kwargs)

            # save for later use
            self._instances_dict[cleaned_instance_name] = instance

            return instance
