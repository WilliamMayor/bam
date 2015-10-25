import os
import sys

from sqlalchemy import create_engine

from models import Base

if 'db' in sys.argv:
    if 'init' in sys.argv:
        engine = create_engine(os.environ['DATABASE_URL'])
        Base.metadata.create_all(engine)
