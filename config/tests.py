from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_check_returns_ok(self):
        # Production forces HTTPS; exercise the endpoint under the same
        # transport condition to avoid an expected HTTP-to-HTTPS redirect.
        response = self.client.get(reverse('health-check'), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
