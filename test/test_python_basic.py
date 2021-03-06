import unittest
import unit

class TestUnitBasic(unit.TestUnitControl):

    def setUpClass():
        unit.TestUnit().check_modules('python')

    def test_python_get(self):
        resp = self.get()
        self.assertEqual(resp, {'listeners': {}, 'applications': {}}, 'empty')
        self.assertEqual(self.get('/listeners'), {}, 'empty listeners prefix')
        self.assertEqual(self.get('/applications'), {},
            'empty applications prefix')

        self.put('/applications', """
            {
                "app": {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """)

        resp = self.get()

        self.assertEqual(resp['listeners'], {}, 'python empty listeners')
        self.assertEqual(resp['applications'],
            {
                "app": {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
             },
             'python applications')

        self.assertEqual(self.get('/applications'),
            {
                "app": {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module":"wsgi"
                }
            },
            'python applications prefix')

        self.assertEqual(self.get('/applications/app'),
            {
                "type": "python",
                "workers": 1,
                "path": "/app",
                "module": "wsgi"
            },
            'python applications prefix 2')

        self.assertEqual(self.get('/applications/app/type'), 'python',
            'python applications type')
        self.assertEqual(self.get('/applications/app/workers'), 1,
            'python applications workers')

        self.put('/listeners', '{"*:7080":{"application":"app"}}')

        self.assertEqual(self.get()['listeners'],
            {"*:7080":{"application":"app"}}, 'python listeners')
        self.assertEqual(self.get('/listeners'),
            {"*:7080":{"application":"app"}}, 'python listeners prefix')
        self.assertEqual(self.get('/listeners/*:7080'),
            {"application":"app"}, 'python listeners prefix 2')
        self.assertEqual(self.get('/listeners/*:7080/application'), 'app',
            'python listeners application')

    def test_python_put(self):
        self.put('/', """
            {
                "listeners": {
                    "*:7080": {
                        "application": "app"
                    }
                },
                "applications": {
                    "app": {
                        "type": "python",
                        "workers": 1,
                        "path": "/app",
                        "module": "wsgi"
                    }
                }
            }
            """)

        resp = self.get()

        self.assertEqual(resp['listeners'], {"*:7080":{"application":"app"}},
            'put listeners')

        self.assertEqual(resp['applications'],
            {
                "app": {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
            },
            'put applications')

        self.put('/listeners', '{"*:7081":{"application":"app"}}')
        self.assertEqual(self.get('/listeners'),
            {"*:7081": {"application":"app"}}, 'put listeners prefix')

        self.put('/listeners/*:7082', '{"application":"app"}')

        self.assertEqual(self.get('/listeners'),
            {
                "*:7081": {
                    "application": "app"
                },
                "*:7082": {
                    "application": "app"
                }
            },
            'put listeners prefix 3')

        self.put('/applications/app/workers', '30')
        self.assertEqual(self.get('/applications/app/workers'), 30,
            'put applications workers')

        self.put('/applications/app/path', '"/www"')
        self.assertEqual(self.get('/applications/app/path'), '/www',
            'put applications path')

    def test_python_delete(self):
        self.put('/', """
            {
                "listeners": {
                    "*:7080": {
                        "application": "app"
                    }
                },
                "applications": {
                    "app": {
                        "type": "python",
                        "workers": 1,
                        "path": "/app",
                        "module": "wsgi"
                    }
                }
            }
            """)

        self.assertIn('error', self.delete('/applications/app'),
            'delete app before listener')
        self.assertIn('success', self.delete('/listeners/*:7080'),
            'delete listener')
        self.assertIn('success', self.delete('/applications/app'),
            'delete app after listener')
        self.assertIn('error', self.delete('/applications/app'),
            'delete app again')

if __name__ == '__main__':
    unittest.main()
