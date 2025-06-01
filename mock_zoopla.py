class Zoopla:
    def __init__(self, api_key=None, verbose=False):
        self.api_key = api_key
        self.verbose = verbose

    def average_area_sold_price(self, params):
        postcode = params.get('area', 'UNKNOWN')
        print(f"[MOCK] Returning average sold price for {postcode}")
        return {
            'average_sold_price_5year': 285000,
            'average_sold_price': 275000
        }