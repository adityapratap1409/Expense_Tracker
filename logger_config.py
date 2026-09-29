import logging


def init_log(fname="expense_tracker.log"):
    logging.basicConfig(
        filename=fname, level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
