"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError  # throws when db is not ready


class Command(BaseCommand):
    """ Django command to wait for the database. """

    def handle(self, *args, **options):
        """ Entrypoint for command. """
        self.stdout.write('Waiting for database...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])  # is db ready?
                db_up = True  # if it is ready
            except (Psycopg2Error, OperationalError):  # if it isn't ready
                self.stdout.write('Database is unavailable, \
                     waiting 1 second...')
                time.sleep(1)  # wait for a second and try again

        self.stdout.write(self.style.SUCCESS('Database is available!'))
