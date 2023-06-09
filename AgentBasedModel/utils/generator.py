import itertools
from typing import List, Dict


class ConfigGenerator:
    def __init__(self, **kwargs):
        self.scenarios = kwargs.get("scenarios", dict())
        self.result = {}

    def generate(self, **kwargs) -> Dict:
        for scenario, config in self.scenarios.items():
            self.result[scenario] = self.generate_scenario(**kwargs, **config)
        return self.result

    def generate_scenario(self, **kwargs) -> list:
        events = kwargs.get("events", list())
        base_market_makers = kwargs.get("base_market_makers", list())
        nn_market_makers = kwargs.get("nn_market_makers", list())
        market_makers = nn_market_makers + base_market_makers
        chartists = kwargs.get("chartists", list())
        randoms = kwargs.get("randoms", list())
        fundamentalists = kwargs.get("fundamentalists", list())
        probe_agents = kwargs.get("probe_agents", list())
        size = kwargs.get("size", 10)
        stability_threshold = kwargs.get("stability_threshold", 5)
        iterations = kwargs.get("iterations", 1)
        window = kwargs.get("window", 5)
        configs = list()
        for events in itertools.product(*[*events]):
            for traders in itertools.product(*[*market_makers, *chartists, *randoms, *fundamentalists, *probe_agents]):
                configs.append(
                    {
                        "exchanges": [
                            {
                                "volume": 2000
                            }
                        ],
                        "events": list(events),
                        "traders": list(traders),
                        "size": size,
                        "window": window,
                        "stability_threshold": stability_threshold,
                        "iterations": iterations,
                    }
                )
        return configs


def generate_configs(**kwargs) -> Dict:
    base_event = {
        "type": "MarketPriceShock",
        "it": 200,
        "price_change": 0,
        "stock_id": 0
    }
    base_market_maker = {
        "count": 5,
        "type": "MarketMaker",
        "cash": 10000,
        "markets": [
            0
        ],
        "softlimits": [
            100
        ],
        "assets": [
            0
        ],
        "stub_quotes_enabled": False,
        "stub_size": 30,
        "nn_enabled": False,
        "delay_enabled": True,
        "delay": 1
    }
    nn_market_maker = {
        "count": 5,
        "type": "MarketMaker",
        "cash": 10000,
        "markets": [
            0
        ],
        "softlimits": [
            100
        ],
        "assets": [
            0
        ],
        "stub_quotes_enabled": False,
        "stub_size": 30,
        "nn_enabled": True,
        "delay_enabled": True,
        "delay": 1
    }
    base_chartist = {
        "count": 10,
        "type": "Chartist",
        "cash": 1000,
        "markets": [
            0
        ],
        "assets": [
            0
        ],
        "delay_enabled": False,
        "delay": 1
    }
    base_random = {
        "count": 10,
        "type": "Random",
        "markets": [
            0
        ],
        "cash": 1000,
        "assets": [
            0
        ],
        "delay_enabled": False,
        "delay": 1
    }
    base_fundamentalist = {
        "count": 10,
        "type": "Fundamentalist",
        "markets": [0],
        "cash": 1000,
        "assets": [0],
        "delay_enabled": False,
        "delay": 1
    }
    base_probe_agent = {
        "count": 1,
        "type": "ProbeAgent",
        "markets": [0],
        "cash": 0,
        "assets": [0],
        "delay_enabled": False,
        "delay": 1
    }
    scenarios = {
        # "no_nn": {
        #     "events": [
        #         [{
        #             **base_event,
        #             "price_change": price_change,
        #         } for price_change in [0]],
        #     ],
        #     "base_market_makers": [
        #         [{
        #             **base_market_maker,
        #             "count": count,
        #         } for count in [5]]
        #     ],
        #     "nn_market_makers": [
        #         [{
        #             **nn_market_maker,
        #             "count": count,
        #         } for count in [5]]
        #     ],
        #     "chartists": [
        #         [{
        #             **base_chartist,
        #             "count": count,
        #         } for count in [25]]
        #     ],
        #     "randoms": [
        #         [{
        #             **base_random,
        #             "count": count,
        #         } for count in [25]]
        #     ],
        #     "fundamentalists": [
        #         [{
        #             **base_fundamentalist,
        #             "count": count,
        #         } for count in [16]]
        #     ],
        #     "probe_agents": [
        #         [{
        #             **base_probe_agent,
        #             "count": count,
        #         } for count in [0]]
        #     ],
        # },
        "hpe": {
            "events": [
                [{
                    **base_event,
                    "price_change": price_change,
                } for price_change in [0]],
            ],
            "base_market_makers": [
                [{
                    **base_market_maker,
                    "count": count,
                } for count in [0]]
            ],
            "nn_market_makers": [
                [{
                    **nn_market_maker,
                    "count": count,
                } for count in [5]]
            ],
            "chartists": [
                [{
                    **base_chartist,
                    "count": count,
                } for count in [5]]
            ],
            "randoms": [
                [{
                    **base_random,
                    "count": count,
                } for count in [15]]
            ],
            "fundamentalists": [
                [{
                    **base_fundamentalist,
                    "count": count,
                } for count in [6]]
            ],
            "probe_agents": [
                [{
                    **base_probe_agent,
                    "count": count,
                } for count in [1]]
            ],
        },
    }
    generator = ConfigGenerator(scenarios=scenarios)
    return generator.generate(**kwargs)
