import os
import MySQLdb
from abc import ABC, abstractmethod

from django.conf import settings


class Connection(ABC):
    """
    Base class interface for connecting to a database server.
    We need two different connections since our engine, that is responsible for handling the video uploads and processing
    is not part of the django database.
    """
    @abstractmethod
    def get_db_connection(self) -> MySQLdb.Connection:
        """
        Abstract method to implement a Mysqldb Connection object instance
        """
        pass


class DjangoConnection(Connection):
    """
    Database connection for connecting to the django server
    """

    def get_db_connection(self):
        repo_db_connection = MySQLdb.Connection(host=settings.DATABASES['default']['HOST'],
                                                port=settings.DATABASES['default']['PORT'],
                                                user=settings.DATABASES['default']['USER'],
                                                passwd=settings.DATABASES['default']['PASSWORD'],
                                                db=settings.DATABASES['default']['NAME'],
                                                )
        return repo_db_connection
