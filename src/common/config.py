global logger
import datetime
import json
import logging


tracer = logging.getLogger("config")
tracer.setLevel(logging.CRITICAL)  # or desired level
tracer.addHandler(logging.FileHandler("indexer.log"))


class Config:
    """A python singleton"""

    # Usage example
    # Config().write_log('INFO', 'train_metric', context_dict=elastic_train_metrics)

    class __impl:
        """Implementation of the singleton interface"""

        def __init__(self):
            self._start_time = datetime.datetime.utcnow().strftime("%d-%m-%y_%H:%M")
            self._config = {"config_path": "", "use_wandb": False, "use_elastic": False}

        def load(self, config_path):
            """
            Loads a full config jsonnet
            """
            with open(config_path) as f:
                self._config.update(json.load(f))

        def override_dict(self, new_config):
            """
            Adds a value to the config if missing, or overrides if already in config
            key: string path in config separated by '.' e.g. training_arguments.num_train_epochs
            """
            for key, val in new_config.items():
                tokens = key.split(".")
                config_internal = self._config
                for token in tokens[:-1]:
                    if token in config_internal:
                        config_internal = config_internal[token]
                    else:
                        raise (ValueError(f"could not find {key} in config!"))

                if tokens[-1] in config_internal:
                    if val is not None:
                        if val == "False":
                            config_internal[tokens[-1]] = False
                        elif val == "True":
                            config_internal[tokens[-1]] = True
                        else:
                            config_internal[tokens[-1]] = val
                else:
                    raise (ValueError(f"could not find {key} in config!"))

        def add_value(self, key, value):
            """
            Adds a value to the config if missing, or overrides if already in config
            key: string path in config separated by '.' e.g. training_arguments.num_train_epochs
            """
            pass

        def iter_on_config(self, d, key, full_key=""):
            entries = []
            vals = []
            val = None
            for k, v in d.items():
                if isinstance(v, dict):
                    if key in v:
                        vals.append(v[key])
                        keys.append()
                        return keys, vals
                    else:
                        keys, vals = self.iter_on_config(v, full_key)
                        for i_k, i_v in zip(key, val):
                            vals.append(val)

            return full_key + "." + key, val

        def get(self, key):
            """
            Adds a value to the config if missing, or overrides if already in config
            """
            tokens = key.split(".")
            result = self._config
            for token in tokens[:-1]:
                if token in result:
                    result = result[token]
            if tokens[-1] in result:
                return result[tokens[-1]]
            else:
                # return self.iter_on_config(self._config, key)
                tracer.info(f"could not find {key} in config, return none!")
                return None

            return result

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """Create singleton instance"""
        # Check whether we already have an instance
        if Config.__instance is None:
            # Create and remember instance
            Config.__instance = Config.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__["_Singleton__instance"] = Config.__instance

    def __getattr__(self, attr):
        """Delegate access to implementation"""
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """Delegate access to implementation"""
        return setattr(self.__instance, attr, value)
