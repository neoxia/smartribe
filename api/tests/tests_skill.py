from django.contrib.auth.models import User
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models import SkillCategory, Skill, Evaluation, Request, Offer


class SkillTests(CustomAPITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing skill actions
        """
        user = User(username="user", password="user", email="user@test.fr")
        other = User(username="other", password="other", email="other@test.fr")
        user.save()
        other.save()

        category1 = SkillCategory(name="Cuisine", detail="Tout pour bien manger")
        category2 = SkillCategory(name="Bricolage", detail="Réparations en tout genre")
        category3 = SkillCategory(name="Jardinage", detail="Tailler, planter, bouturer")
        category4 = SkillCategory(name="Informatique", detail="42")
        category1.save()
        category2.save()
        category3.save()
        category4.save()

        skill1 = Skill(user=user, category=category1, description="", level=2)
        skill2 = Skill(user=user, category=category2, description="", level=1)
        skill3 = Skill(user=user, category=category3, description="", level=2)
        skill4 = Skill(user=other, category=category2, description="", level=3)
        skill1.save()
        skill2.save()
        skill3.save()
        skill4.save()

        request1 = Request(user=user, category=category2, detail='help1')
        request2 = Request(user=user, category=category2, detail='help2')
        request3 = Request(user=user, category=category4, detail='help2')
        request1.save()
        request2.save()
        request3.save()

        offer1 = Offer(user=other, request=request1, skill=skill4, detail='no problem1')
        offer2 = Offer(user=other, request=request2, skill=skill4, detail='no problem2')
        offer3 = Offer(user=other, request=request3, detail='no problem2')
        offer1.save()
        offer2.save()
        offer3.save()

        evaluation1 = Evaluation(offer=offer1, mark=3, comment='good')
        evaluation2 = Evaluation(offer=offer2, mark=4, comment='good')
        evaluation3 = Evaluation(offer=offer3, mark=2, comment='good')
        evaluation1.save()
        evaluation2.save()
        evaluation3.save()

    def test_create_skill_without_auth(self):
        """
        Ensure a non authenticated visitor cannot create a skill
        """
        url = '/api/v1/skills/'
        data = {
            'user': 1,
            'category': 1,
            'description': 'test category'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_my_skills(self):
        """
        Ensure a non authenticated visitor cannot create a skill
        """
        url = '/api/v1/skills/0/list_my_skills/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(3, data['count'])
        self.assertEqual(0, data['results'][0]['mark_count'])
        self.assertIsNone(data['results'][0]['avg_mark'])
        self.assertEqual('Cuisine', data['results'][0]['category_name'])


    def test_retrieve_others_skills(self):
        """
        Ensure a non authenticated visitor cannot create a skill
        """
        url = '/api/v1/skills/'
        data = {
            'user__id': 2
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(2, data['results'][0]['mark_count'])
        self.assertEqual(3.5, data['results'][0]['avg_mark'])
        self.assertEqual('Bricolage', data['results'][0]['category_name'])
