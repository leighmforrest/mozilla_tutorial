from django.test import TestCase


class YourTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method
        self.bleen = 1

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_something_that_will_pass(self):
        self.assertTrue(self.bleen == 1)

    def test_something_that_will_fail(self):
        self.assertFalse(self.bleen == 2)
