class MockDB:
    def __init__(self):
        self.test_data_add = None
        self.test_timestamp = None
        self.test_all_timestamps = None

    def add(self, data):
        self.test_data_add = data

    def newest_timestamp(self):
        return self.test_timestamp


    def fetch_timestamps(self):
        return iter(self.test_all_timestamps)