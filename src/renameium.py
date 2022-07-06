#!/usr/bin/env python3

import logging

import config;

def main():
    config = config.general_config()
    logging.basicConfig(filename=config['log_file'], level=logging.INFO)