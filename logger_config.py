import logging


# logs to file so stdout/terminal doesn't get cluttered
def init_log(fname="expense_tracker.log"):
    logging.basicConfig(
        filename=fname,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
