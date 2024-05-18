import unittest
from tests.test_base import BaseTestCase

class SurveyDashboardTestCase(BaseTestCase):
    def test_dashboard_page(self):
        response = self.client.get('/survey-dashboard')
        self.assertEqual(response.status_code, 200)

        # Check if the page itself rendered correctly
        self.assertIn(b'Survey Dashboard', response.data)
        
        # Check that surveys are in the response data
        self.assertIn(b'Survey 1', response.data)
        self.assertIn(b'Survey 2', response.data)

if __name__ == '__main__':
    unittest.main()
