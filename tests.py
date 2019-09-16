import json
import requests
import unittest


class TestApp(unittest.TestCase):
    url = 'http://localhost:8080/'

    def test_json_request(self):

        data = {}
        with open('testcases/sample.html', encoding="utf-8") as html:
            data["contents"] = html.read()

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_file_input(self):

        file_contents = ""
        with open('testcases/sample.html', 'rb') as f:
            file_contents = f.read()

        response = requests.post(url=self.url, files={'file': file_contents})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_neither_json_not_file_input(self):
        data = {

        }
        response = requests.post(url=self.url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_blank_file_input(self):
        # blank pdf will be the output
        file_contents = ""
        with open('testcases/blank.html', 'rb') as f:
            file_contents = f.read()

        response = requests.post(url=self.url, files={'file': file_contents})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_content_with_blank_html(self):
        data = {
            'contents': '<html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body></body></html>',
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_html_with_unicode_char(self):
        
        data = {}
        with open('testcases/unicode.html', encoding="utf-8") as f:
            data["contents"] = f.read()
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=self.url, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_get_endpoint(self):
        response = requests.get(
            url='http://localhost:8080/ping',
        )
        self.assertEqual(response.status_code, 200)

    def test_get_endpoint_with_invalid_url(self):
        response = requests.get(
            url='http://localhost:8080/random',
        )
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
