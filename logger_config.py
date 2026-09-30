import logging
import os

# quick logger setup
_log_done = False

def init_log(fname="expense_tracker.log"):
    global _log_done
    # don't init multiple times
    if _log_done == True:
        return
    
    log_fmt = "%(asctime)s - %(levelname)s - %(message)s"
    try:
        logging.basicConfig(
            filename=fname, 
            level=logging.INFO,
            format=log_fmt
        )
        _log_done = True
    except Exception as err:
        # fallback if file write fails
        print("warning: failed to init log file %s: %s" % (fname, str(err)))
