class DatasetReader:
    """
    info-seeking dataset reader
    """

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def read(self, rand_sample=None):
        raise NotImplementedError("Please Implement this method")

    def parse_example(self, example):
        raise NotImplementedError("Please Implement this method")
