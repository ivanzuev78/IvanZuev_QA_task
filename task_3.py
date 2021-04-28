import logging
import os
import time
from abc import abstractmethod
from random import randbytes

import psutil


def get_logger(name=__file__, file="log.txt", encoding="utf-8"):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )
    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


class StopTestCase(Exception):
    pass


class TestCaseTemplate:
    def __init__(self, tc_id: int, name: str, logger: logging.Logger):
        self.tc_id = tc_id
        self.name = name
        self.logger = logger

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
    def __init__(self, tc_id, name, logger):
        super().__init__(tc_id, name, logger)

    def prep(self):
        self.logger.info("TestCaseOne - prep started")
        cur_time = int(time.time())
        if cur_time % 2 == 1:
            raise StopTestCase(f"Time = {cur_time}\nStop testcase")

    def run(self):
        self.logger.info("TestCaseOne - run started")
        print(os.listdir(path="."))

    def clean_up(self):
        pass

    def execute(self):
        self.logger.info("TestCaseOne - execute started")
        try:
            self.prep()
        except StopTestCase as e:
            self.logger.warning(f"TestCaseOne - prep failed! \n{e}")
        try:
            self.run()
        except Exception as e:
            self.logger.warning(f"TestCaseOne - run failed! \n{e}")


class TestCaseTwo(TestCaseTemplate):
    def __init__(self, tc_id, name, logger):
        super().__init__(tc_id, name, logger)

    def prep(self):
        self.logger.info("TestCaseTwo - prep started")
        if psutil.virtual_memory().total / (2 ** 30) < 1:
            raise StopTestCase("There is not enough virtual_memory")

    def run(self):
        self.logger.info("TestCaseTwo - run started")
        with open("test", "wb") as f:
            f.write(randbytes(2 ** 20))

    def clean_up(self):
        self.logger.info("TestCaseTwo - clean_up started")
        os.remove("test")

    def execute(self):
        self.logger.info("TestCaseTwo - execute started")
        try:
            self.prep()
        except StopTestCase as e:
            self.logger.warning(f"TestCaseTwo - prep failed! \n{e}")
        try:
            self.run()
        except FileNotFoundError as e:
            self.logger.warning(f"TestCaseTwo - run failed! \n{e}")
        try:
            self.clean_up()
        except FileNotFoundError as e:
            self.logger.warning(f"TestCaseTwo - clean_up failed! \n{e}")


if __name__ == "__main__":

    my_logger = get_logger()

    my_logger.info("Program started")

    test1 = TestCaseOne(tc_id=1, name="test_1", logger=my_logger)
    test2 = TestCaseTwo(tc_id=2, name="test_2", logger=my_logger)
    test1.execute()
    test2.execute()

    my_logger.info("Program finished\n")
