from .main import Database
from ..settings import database_name

database = Database(database_name)

from .basictable import BasicTable