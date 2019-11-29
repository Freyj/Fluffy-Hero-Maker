import unittest

from databases.dnd5.dnd5_db import drop_all_tables, create_dnd5_db
from databases.dnd5.dnd5_languages_db import insert_dnd5_language, get_all_unrestricted_languages


class TestLanguages(unittest.TestCase):
    def test_getting_all_unrestricted_languages(self):
        """
            Testing that Druidic does not show up for dnd5 languages as it is restricted to druids
        """
        drop_all_tables()
        create_dnd5_db()
        insert_dnd5_language()
        names = get_all_unrestricted_languages()
        assert("Druidic" not in names)
