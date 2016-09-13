import json
import tempfile
import logging
import time

from werkzeug.wsgi import wrap_file
from werkzeug.wrappers import Request, Response
from executor import execute

logger = logging.getLogger(__name__)


@Request.application
def application(request):
    """
    To use this application, the user must send a POST request with
    base64 or form encoded encoded HTML content and the wkhtmltopdf Options in
    request data, with keys 'base64_html' and 'options'.
    The application will return a response with the PDF file.
    """
    start = time.time()
    if request.method != 'POST':
        return Response(
            status=405
        )
    request_is_json = False
    if request.content_type == 'application/json':
        request_is_json = True

    with tempfile.NamedTemporaryFile(suffix='.html') as source_file:

        if request_is_json:
            # If a JSON payload is there, all data is in the payload
            payload = json.loads(request.data)
            try:
                source_file.write(payload['contents'].decode('base64'))
            except KeyError:
                logger.warn('The request content is not specified')
                return Response(
                    status=400
                )
            options = payload.get('options', {})
        elif request.files:
            # First check if any files were uploaded
            source_file.write(request.files['file'].read())
            # Load any options that may have been provided in options
            options = json.loads(request.form.get('options', '{}'))
        else:
            logging.warn('The request was neither json, not had files, cannot convert.')
            return Response(
                status=400
            )

        source_file.flush()

        # Evaluate argument to run with subprocess
        args = ['wkhtmltopdf']

        # Add Global Options
        if options:
            for option, value in options.items():
                args.append('--%s' % option)
                if value:
                    args.append('"%s"' % value)

        # Add source file name and output file name
        file_name = source_file.name
        args += [file_name, file_name + ".pdf"]

        # Execute the command using executor
        execute(' '.join(args))
        end = time.time()
        print "time taken {elapse}".format(elapse=(end-start))
        return Response(
            wrap_file(request.environ, open(file_name + '.pdf')),
            mimetype='application/pdf',
        )


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 8080, application
    )
