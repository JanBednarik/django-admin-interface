import random
import shutil
from unittest import expectedFailure

from django.conf import settings
from django.test import TestCase, TransactionTestCase

from admin_interface.models import Theme


class AdminInterfaceModelsTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Theme.objects.all().delete()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def __test_active_theme(self):
        theme = Theme.get_active_theme()
        print(theme)
        self.assertTrue(theme is not None)
        self.assertTrue(theme.active)
        self.assertEqual(Theme.objects.filter(active=True).count(), 1)

    def test_default_theme_created_if_no_themes(self):
        Theme.objects.all().delete()
        self.__test_active_theme()

    def test_default_theme_created_if_all_themes_deleted(self):
        Theme.objects.all().delete()
        self.__test_active_theme()

    def test_default_theme_activated_on_save_if_no_active_themes(self):
        Theme.objects.all().delete()
        theme = Theme.get_active_theme()
        theme.active = False
        theme.save()
        self.__test_active_theme()

    def test_default_theme_activated_after_update_if_no_active_themes(self):
        Theme.objects.all().delete()
        Theme.objects.all().update(active=False)
        self.__test_active_theme()

    def test_default_theme_activated_after_update_if_multiple_active_themes(self):
        Theme.objects.all().delete()
        theme_1 = Theme.objects.create(name="Custom 1", active=True)
        theme_2 = Theme.objects.create(name="Custom 2", active=True)
        theme_3 = Theme.objects.create(name="Custom 3", active=True)
        Theme.objects.update(active=False)
        Theme.objects.update(active=True)
        self.__test_active_theme()

    def test_default_theme_activated_on_active_theme_deleted(self):
        Theme.objects.all().delete()
        theme_1 = Theme.objects.create(name="Custom 1", active=True)
        theme_2 = Theme.objects.create(name="Custom 2", active=True)
        theme_3 = Theme.objects.create(name="Custom 3", active=True)
        Theme.objects.filter(pk=Theme.get_active_theme().pk).delete()
        self.__test_active_theme()

    def test_last_theme_activated_on_multiple_themes_created(self):
        Theme.objects.all().delete()
        theme_1 = Theme.objects.create(name="Custom 1", active=True)
        theme_2 = Theme.objects.create(name="Custom 2", active=True)
        theme_3 = Theme.objects.create(name="Custom 3", active=True)
        self.assertEqual(Theme.get_active_theme().pk, theme_3.pk)
        self.__test_active_theme()

    def test_last_theme_activated_on_multiple_themes_activated(self):
        Theme.objects.all().delete()
        theme_1 = Theme.objects.create(name="Custom 1", active=True)
        theme_2 = Theme.objects.create(name="Custom 2", active=True)
        theme_3 = Theme.objects.create(name="Custom 3", active=True)
        theme_4 = Theme.objects.create(name="Custom 4", active=True)
        theme_5 = Theme.objects.create(name="Custom 5", active=True)
        themes = [theme_1, theme_2, theme_3, theme_4, theme_5]
        for i in range(5):
            random.shuffle(themes)
            for theme in themes:
                theme.set_active()
                self.assertEqual(Theme.get_active_theme().pk, theme.pk)
        self.__test_active_theme()

    def test_repr(self):
        theme = Theme.get_active_theme()
        self.assertEqual(repr(theme), "<Theme: Django>")

    def test_str(self):
        theme = Theme.get_active_theme()
        self.assertEqual(str(theme), "Django")


# class AdminInterfaceModelsMultiDBTestCase(TestCase):
#     databases = ["default", "replica"]

#     @classmethod
#     def setUpTestData(cls):
#         Theme.objects.create(name="Change Active", active=True)

#     def test_get_theme_from_default_db(self):
#         de_theme = Theme.get_active_theme()
#         assert de_theme.name == "Change Active"

#     def test_get_theme_from_replica_db(self):
#         replica_theme = Theme.get_active_theme(database="replica")
#         assert replica_theme.name == "Django"

#     def test_db_are_isolated(self):
#         default_theme = Theme.get_active_theme()
#         replica_theme = Theme.get_active_theme(database="replica")
#         assert default_theme.name != replica_theme.name

#     @expectedFailure
#     def test_fail_for_wrong_db_defined_in_kwargs(self):
#         Theme.get_active_theme(database="other")
