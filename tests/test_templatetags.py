from django.test import TestCase, RequestFactory

from task.templatetags.query_transformer import query_transform


class TemplateTagsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_query_transform(self):
        request = self.factory.get(
            "/some-url/", {"param1": "value1", "param2": "value2"}
        )
        updated_query = query_transform(request, param3="value3")
        self.assertEqual(
            updated_query,
            "param1=value1&param2=value2&param3=value3"
        )
