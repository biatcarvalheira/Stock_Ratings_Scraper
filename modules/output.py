import pandas as pd
import time
import os
import datetime
import sys


def clean_lists(*lists):
    for lst in lists:
        lst.clear()


