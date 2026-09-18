import json
from pathlib import Path


class ExpertSystem:
    def __init__(self):
        CURRENT_DIR = Path(__file__).parent

        file_path = CURRENT_DIR / ".." / "data" / "assets.json" 

        with open(file_path, "r") as f:
            self.data = json.load(f)

        self.rating = {asset['name'] + ' (' + asset['asset'] + ')': (asset, 0.0) for asset in self.data['assets']}

        self.weights = {
            "market": 0.2,
            "risk": 0.2,
            "asset": 0.3,
            "parameter": 0.06,
            "liquidity": 0.04,
            "horizon": 0.1,
            'investor_qualification': 0.1
        }

        self.assets_match = {
            'Акция': ['Криптовалюта', 'Опцион', '', 'Фьючерс', 'Валюта', '', '', 'Фонд недвижимости', '', 'Облигация', '', '', '', '', 'Акция'],
            'Облигация': ['Криптовалюта', 'Опцион', '', 'Фьючерс', 'Валюта', '', '', 'Фонд недвижимости', '', 'Акция', '', '', '', '', 'Облигация'],
            'Валюта': ['Фонд недвижимости', 'Облигация', 'Опцион', '', 'Фьючерс', '', 'Акция', '', '', 'Криптовалюта', '', '', '', '', 'Валюта'],
            'Криптовалюта': ['Фонд недвижимости', '', 'Облигация', 'Акция', '', 'Опцион', 'Фьючерс', '', '', 'Валюта', '', '', '', '', 'Криптовалюта'],
            'Фьючерс': ['Фонд недвижимости', 'Облигация', 'Акция', '', 'Валюта', '', 'Криптовалюта', '', '', 'Опцион', '', '', '', '', 'Фьючерс'],
            'Опцион': ['Фонд недвижимости', '', 'Облигация', 'Акция', '', 'Валюта', 'Криптовалюта', '', '', 'Фьючерс', '', '', '', '', 'Опцион'],
            'Фонд недвижимости': ['Криптовалюта', 'Опцион', 'Фьючерс', 'Валюта', '', '', 'Облигация', '', 'Акция', '', '', '', '', '', 'Фонд недвижимости']
        }


    def evaluate(self, user_input: dict):
        max_match = 0

        for crit, val in user_input.items():
            if val != '' and val != 0:
                max_match += self.weights[crit]

        for asset_name, asset in self.rating.items():
            asset_info = asset[0]
            rate = 0
            coef = 1

            if asset_info['risk'] == user_input['risk']:
                rate += self.weights['risk']

            if user_input['asset'] != '':
                asset_coef = self.assets_match[asset_info['asset']].index(user_input['asset']) / 14

                if asset_coef == 0:
                    asset_coef = 1

                rate += asset_coef * self.weights['asset']

            #parameter
            if user_input['parameter'] != 0 and asset_info['parameter'] != '-':
                dist = abs((user_input['parameter'] - float(asset_info['parameter'][0:-1])) / user_input['parameter'])
                if dist > 1:
                    dist = 1

                dist_coef = self.weights['parameter'] * dist * -1
                rate += self.weights['parameter'] + dist_coef

            if asset_info['liquidity'] == user_input['liquidity']:
                rate += self.weights['liquidity']

            if asset_info['horizon'] == "Среднесрочный/Долгосрочный":
                if user_input['horizon'] == "Среднесрочный" or user_input['horizon'] == "Долгосрочный":
                    rate += self.weights['horizon']

            if asset_info['horizon'] == "Краткосрочный/Среднесрочный":
                if user_input['horizon'] == "Среднесрочный" or user_input['horizon'] == "Краткосрочный":
                    rate += self.weights['horizon']

            elif asset_info['horizon'] == user_input['horizon']:
                rate += self.weights['horizon']

            if asset_info['market'] == user_input['market']:
                rate += self.weights['market']
            elif user_input['market'] != '':
                coef = 0

            if user_input['investor_qualification'].lower() == 'нет' and asset_info['investor_qualification'].lower() == 'да':
                coef = 0
            elif user_input['investor_qualification'] != '':
                rate += self.weights['investor_qualification']

            rate *= coef

            self.rating[asset_name] = (asset_info, rate)

        return dict(sorted(self.rating.items(), key=lambda item: item[1][1], reverse=True)), max_match


    def return_names(self):
        return [asset['name'] + ' (' + asset['asset'] + ')' for asset in self.data['assets']]


    def return_markets(self):
        markets = list(set(asset["market"] for asset in self.data['assets']))
        return markets


    def return_assets(self):
        assets = list(set(book["asset"] for book in self.data['assets']))
        return assets
