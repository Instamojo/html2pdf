import json
import requests
import unittest


class TestApp(unittest.TestCase):
    url = 'http://localhost:12345/'

    def test_json_request(self):
        data = {
            'contents': open('testcases/sample.html').read().encode('base64'),
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_with_null_json_request(self):
        data = {
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_with_non_html_input(self):
        data = {
            'contents': 'random non html string... test test test',
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 500)

    def test_file_input(self):
        files = {'file': open('testcases/sample.html', 'rb')}
        response = requests.post(url=self.url, files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_neither_json_not_file_input(self):
        data = {

        }
        response = requests.post(url=self.url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_blank_file_input(self):
        # blank pdf will be the output
        files = {'file': open('testcases/blank.html', 'rb')}
        response = requests.post(url=self.url, files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')


if __name__ == '__main__':
    unittest.main()
