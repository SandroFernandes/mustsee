from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import IntegrityError
from testing_demo import DemoTestCase
from .models import Attraction, UserRank

def make_attraction(name, url=''):
    return Attraction.objects.create(name=name, url=url)

def rank(attraction, session_uuid, rank=None):
    return UserRank.objects.create(
        attraction=attraction,
        session_uuid=session_uuid, rank=rank)

class SimpleTest(DemoTestCase):
    def setUp(self):
        self.cbd = make_attraction('CBD')
        self.mona = make_attraction('MONA')
        self.lark = make_attraction('Lark Distillery')

    def test_user_rank(self):
        a = rank(self.lark, 'A')
        self.assertEqual(a.rank, 0)
        b = rank(self.cbd, 'A')
        self.assertEqual(b.rank, 1)
        c = rank(self.cbd, 'B')
        self.assertEqual(c.rank, 0)

    def test_duplicate_rank(self):
        a = rank(self.lark, 'A')
        self.assertEqual(a.rank, 0)
        with self.assertRaises(IntegrityError):
            b = rank(self.lark, 'A')
            self.assertEqual(b.rank, 1)

    def test_attraction_list(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mustsee/list.html')
        self.assertContains(response, 'Must See')
        self.assertEqual(
            response.context['attractions'],
            [self.cbd, self.lark, self.mona]
        )
        self.assertQuerysetEqual(
            response.context['attractions'],
            [None, None, None],
            lambda a: a.user_rank
        )
        self.assertQuerysetEqual(
            response.context['attractions'],
            [0, 0, 0],
            lambda a: a.overall_rank
        )

        response = self.client.get(
            reverse('promote', args=(self.lark.pk,)),
            follow=True
        )
        self.assertRedirects(response, reverse('list'))

        self.assertEqual(
            response.context['attractions'],
            [self.lark, self.cbd, self.mona]
        )
        self.assertQuerysetEqual(
            response.context['attractions'],
            [0, None, None],
            lambda a: a.user_rank
        )
        self.assertQuerysetEqual(
            response.context['attractions'],
            [0, 1, 1],
            lambda a: a.overall_rank
        )

    def test_admin(self):
        self.create_user('super', super=True)
        self.login('super')
        self._test_admin((Attraction, UserRank))
