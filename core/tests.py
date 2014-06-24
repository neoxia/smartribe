from django.test import TestCase
from core.models import Community


class CommunityTestCase(TestCase):
    def setUp(self):
        Community.objects.create(name="RER D")

    def test_community_str(self):
        comm = Community.objects.get(name="RER D")
        self.assertEqual(comm.__str__(), "RER D")
