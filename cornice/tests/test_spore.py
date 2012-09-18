from cornice.tests.support import TestCase

from cornice.service import Service, get_services
from cornice.sporehook import generate_spore


class TestSporeHook(TestCase):
    def test_sporehook(self):

        coffees = Service(name='coffees', path='/coffee')
        coffee = Service(name='coffee', path='/coffee/{id}')

        @coffees.get()
        def get_coffees(request):
            """Get the coffee"""
            return "ok"

        @coffees.post()
        def post_coffees(request):
            """Post information about the coffee"""
            return "ok"

        @coffee.get()
        def get_coffee(request):
            pass

        services = get_services()
        spore = generate_spore(services, name="oh yeah",
                               base_url="http://localhost/", version="1.0")

        # basic fields
        self.assertEqual(spore['name'], "oh yeah")
        self.assertEqual(spore['base_url'], "http://localhost/")
        self.assertEqual(spore['version'], "1.0")

        # methods
        methods = spore['methods']
        self.assertIn('get_coffees', methods)
        self.assertDictEqual(methods['get_coffees'], {
            'path': '/coffee',
            'method': 'GET',
            'format': 'simplejson',
            'description': get_coffees.__doc__
            })

        self.assertIn('post_coffees', methods)
        self.assertDictEqual(methods['post_coffees'], {
            'path': '/coffee',
            'method': 'POST',
            'format': 'simplejson',
            'description': post_coffees.__doc__
            })

        self.assertIn('get_coffee', methods)
        self.assertDictEqual(methods['get_coffee'], {
            'path': '/coffee/:id',
            'method': 'GET',
            'format': 'simplejson',
            'service_params': ('id',)
            })
