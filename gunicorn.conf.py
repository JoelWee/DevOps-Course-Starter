# file gunicorn.conf.py
# coding=utf-8
# Reference: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

loglevel = "info"
errorlog = "./error.log"
accesslog = "./access.log"

bind = "0.0.0.0:5000"
workers = 4

capture_output = True
