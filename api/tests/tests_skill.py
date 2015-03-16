from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models import SkillCategory, Skill, Evaluation, Request, Offer


class SkillTests(CustomAPITestCase):

    user_model = get_user_model()

    def setUp(self):
        """
        Make a user for authenticating and
        testing skill actions
        """
        user = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                              first_name='1', last_name='User', is_active=True)
        other = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)

        category1 = SkillCategory.objects.create(name="Cuisine", detail="Tout pour bien manger")
        category2 = SkillCategory.objects.create(name="Bricolage", detail="Réparations en tout genre")
        category3 = SkillCategory.objects.create(name="Jardinage", detail="Tailler, planter, bouturer")
        category4 = SkillCategory.objects.create(name="Informatique", detail="42")

        skill1 = Skill.objects.create(user=user, category=category1, description="", level=2)
        skill2 = Skill.objects.create(user=user, category=category2, description="", level=1)
        skill3 = Skill.objects.create(user=user, category=category3, description="", level=2)
        skill4 = Skill.objects.create(user=other, category=category2, description="", level=3)

        request1 = Request.objects.create(user=user, category=category2, detail='help1')
        request2 = Request.objects.create(user=user, category=category2, detail='help2')
        request3 = Request.objects.create(user=user, category=category4, detail='help2')

        offer1 = Offer.objects.create(user=other, request=request1, skill=skill4, detail='no problem1')
        offer2 = Offer.objects.create(user=other, request=request2, skill=skill4, detail='no problem2')
        offer3 = Offer.objects.create(user=other, request=request3, detail='no problem2')

        evaluation1 = Evaluation.objects.create(offer=offer1, mark=3, comment='good')
        evaluation2 = Evaluation.objects.create(offer=offer2, mark=4, comment='good')
        evaluation3 = Evaluation.objects.create(offer=offer3, mark=2, comment='good')

    def test_create_skill_without_auth(self):
        """
        Ensure a non authenticated visitor cannot create a skill
        """
        url = '/api/v1/skills/'
        data = {
            'category': 1,
            'description': 'test category'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_skill(self):
        """
        Ensure a non authenticated visitor cannot create a skill
        """
        url = '/api/v1/skills/'
        data = {
            'category': 1,
            'title': 'titre',
            'description': 'test category'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(4, Skill.objects.filter(user__id=1).count())

    def test_retrieve_my_skills(self):
        """
        Ensure a non authenticated visitor cannot create a skill
        """
        url = '/api/v1/skills/0/list_my_skills/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
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

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(2, data['results'][0]['mark_count'])
        self.assertEqual(3.5, data['results'][0]['avg_mark'])
        self.assertEqual('Bricolage', data['results'][0]['category_name'])
