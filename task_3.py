import os
import time
from abc import abstractmethod
from random import randbytes

import psutil


class StopTestCase(Exception):
    pass


class TestCaseTemplate:
    def __init__(self, tc_id: int, name: str):
        self.tc_id = tc_id
        self.name = name

    @abstractmethod
    def prep(self):
        ...

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def clean_up(self):
        ...

    @abstractmethod
    def execute(self):
        ...


class TestCaseOne(TestCaseTemplate):
    def __init__(self, tc_id, name):
        super().__init__(tc_id, name)

    def prep(self):
        cur_time = int(time.time())
        if cur_time % 2 == 1:
            raise StopTestCase(f"Time = {cur_time}\nStop testcase")

    def run(self):
        print(os.listdir(path="."))

    def clean_up(self):
        pass

    def execute(self):
        try:
            self.prep()
            self.run()
        except StopTestCase as e:
            print(e)
            pass


class TestCaseTwo(TestCaseTemplate):
    def __init__(self, tc_id, name):
        super().__init__(tc_id, name)

    def prep(self):
        virtual_memory = psutil.virtual_memory().total / (2 ** 30)
        if virtual_memory < 1:
            raise StopTestCase("There is not enough virtual_memory")

    def run(self):
        with open("test", "wb") as f:
            f.write(randbytes(2 ** 20))

    def clean_up(self):
        os.remove("test")

    def execute(self):
        try:
            self.prep()
            self.run()
            self.clean_up()
        except StopTestCase as e:
            print(e)
            pass
        except FileNotFoundError as e:
            pass


if __name__ == "__main__":
    test1 = TestCaseOne(tc_id=1, name="test_1")
    test2 = TestCaseTwo(tc_id=2, name="test_2")
    test1.execute()
    test2.execute()
