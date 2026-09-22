from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


MARKET_DATA = {
    "ポケモンカード SAR リザードンex 123/099": [
        7000,
        7500,
        8000,
    ],
    "遊戯王 青眼の白龍 レリーフ": [
        15000,
        18000,
        20000,
    ],
}


class MarketAPIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/market":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)

        keyword = params.get("keyword", [""])[0]
        limit = int(params.get("limit", ["100"])[0])

        prices = MARKET_DATA.get(keyword, [])[:limit]

        response = json.dumps({
            "prices": prices
        }).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(response))
        )
        self.end_headers()

        self.wfile.write(response)

    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer(
        ("localhost", 8000),
        MarketAPIHandler,
    )

    print("相場APIテストサーバー起動")
    print("http://localhost:8000/market")
    print("終了するには Ctrl+C")

    server.serve_forever()


if __name__ == "__main__":
    main()
