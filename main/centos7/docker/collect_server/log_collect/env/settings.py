# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数の値を変数に代入
SYSTEM_PATH = os.environ.get("SYSTEM_PATH")
SYSTEM_LOG = os.environ.get("SYSTEM_LOG")
