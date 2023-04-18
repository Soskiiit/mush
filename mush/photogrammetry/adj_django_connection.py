import os
import sys
from pathlib import Path

import django

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(1, str(ROOT_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'mush.settings'
django.setup()
