# HTML to PDF as a service

This service provides a simple HTTP API to convert HTML to a PDF document. It takes a HTML document (not URL) as an input and outputs a PDF document in the response.

Technologies used for this application:

* [Python 3.6](https://docs.python.org/3.6/) - Simple web application and wrapper for wkhtmltopdf
* [Gunicorn](http://gunicorn.org/) - Web server
* [wkhtmltopdf](https://wkhtmltopdf.org/) - HTML to PDF converter engine
* [Google Noto](https://www.google.com/get/noto/) - Fonts for non-ascii characters (like, Tamil, Hindi etc.)

This application is:

* **Synchronous** - Response includes PDF document, which is generated in a blocking manner (without any queuing)
* **Stateless** - No data stored anywhere
* **Scalable** - No single point of failure and no centralised components (since its stateless) making it highly scalable.
