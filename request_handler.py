import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_things, get_one_thing, get_snakes_by_species, create_snake

class HandleRequests(BaseHTTPRequestHandler):
    """handles and fetch calls from client"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query:
            query_params = url_components.query.split("=")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)

    def do_GET(self):
        """handles requests for data from sql db"""
        response = {}
        real_dictionaries = ("owners", "snakes", "species")
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        (resource, id, query_params) = parsed
        if '?' not in self.path and resource in real_dictionaries:

            if id is not None:
                response = get_one_thing(resource, id)
            elif id is None:
                response = get_all_things(resource)

        elif resource == "snakes" and query_params[0] == "species":
            (resource, id, query_params) = parsed

            if query_params[0] == "species" and resource == 'snakes':
                response = get_snakes_by_species(query_params[1])
        else:
            response = False
        if response is False or response == []:
            self._set_headers(404)
        elif response is None:
            self._set_headers(405)
        else:
            self._set_headers(200)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """handles post request for new snake"""

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query) = self.parse_url(self.path)

        new_snake = None

        if resource == "snakes":
            new_snake = create_snake(post_body)
            if len(new_snake) != 6:
                self._set_headers(400)
            else:
                self._set_headers(201)
        else:
            self._set_headers(404)
        self.wfile.write(json.dumps(new_snake).encode())

    def do_PUT(self):
        """Rejects PUT requests to the server"""
        self._set_headers(404)

    def do_DELETE(self):
        """rejects DELETE requests"""
        self._set_headers(404)

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
