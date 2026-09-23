from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


LISTINGS = [
    {
        "id": "mercari001",
        "title": "ポケモンカード SAR リザードンex",
        "price": 5000,
        "shipping_size": 60,
        "shipping_fee": 230,
        "is_large": False,
        "url": "https://example.com/mercari001",
        "is_sold": False,
    },
    {
        "id": "mercari002",
        "title": "ポケモンカード AR ピカチュウ",
        "price": 3000,
        "shipping_size": 60,
        "shipping_fee": 230,
        "is_large": False,
        "url": "https://example.com/mercari002",
        "is_sold": True,
    },
    {
        "id": "mercari003",
        "title": "遊戯王 青眼の白龍 レリーフ",
        "price": 10000,
        "shipping_size": 60,
        "shipping_fee": 230,
        "is_large": False,
        "url": "https://example.com/mercari003",
        "is_sold": False,
    },
]


class MercariAPIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/mercari":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)
        keyword = params.get("keyword", [""])[0]

        items = []

        for listing in LISTINGS:
            if listing["is_sold"]:
                continue

            if keyword:
                if keyword.lower() not in listing["title"].lower():
                    continue

            items.append(listing)

        response = json.dumps(
            {"items": items},
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(response)),
        )
        self.end_headers()

        self.wfile.write(response)

    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer(
        ("localhost", 8001),
        MercariAPIHandler,
    )

    print("商品取得APIテストサーバー起動")
    print("http://localhost:8001/mercari")
    print("終了するには Ctrl+C")

    server.serve_forever()


if __name__ == "__main__":
    main()
