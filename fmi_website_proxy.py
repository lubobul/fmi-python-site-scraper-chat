import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

PORT = 12345

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/static/inject.js':
            # Serve the JavaScript file
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(b"""
                function replaceContent() {
                    var contentTd = document.getElementById('content');
                    if (contentTd) {
                        var iframe = document.createElement('iframe');
                        iframe.src = 'http://localhost:4200';
                        iframe.width = '650';
                        iframe.style.height = '42rem';
                        contentTd.parentNode.replaceChild(iframe, contentTd);
                    }
                }
            """)
        else:
            # Fetch the original website content
            url = 'https://fmi-plovdiv.org/'  # Replace with your target website
            response = requests.get(url)
            content = response.content

            # Parse the HTML and inject your content
            soup = BeautifulSoup(content, 'html.parser')
            inject_content = '<li><a href="#" onclick="replaceContent()">Чат Бот</a></li>'
            menu = soup.find('div', {'id': 'menu'})
            if menu:
                ul = menu.find('ul')
                if ul:
                    ul.append(BeautifulSoup(inject_content, 'html.parser'))

            # Inject the JavaScript reference
            script_tag = soup.new_tag('script', src='http://localhost:12345/static/inject.js')
            soup.body.append(script_tag)

            # Fix CSS and JS paths
            for link in soup.find_all('link', href=True):
                link['href'] = urljoin(url, link['href'])
            for script in soup.find_all('script', src=True):
                script['src'] = urljoin(url, script['src'])
            for img in soup.find_all('img', src=True):
                img['src'] = urljoin(url, img['src'])

            # Serve the modified content
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(soup).encode('utf-8'))

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
