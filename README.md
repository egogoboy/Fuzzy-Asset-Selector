# Fuzzy Asset Selector

A rule-based expert system for selecting financial assets based on an investor's preferences and characteristics.

The project was developed as a university laboratory project to study the application of expert systems to a financial domain. The main focus was on modelling investment-related knowledge and implementing a weighted asset-matching mechanism.

## Overview

**Fuzzy Asset Selector** is a desktop application that evaluates financial assets according to a set of user-defined criteria:

- Market
- Risk level
- Asset type
- Target parameter
- Liquidity
- Investment horizon
- Investor qualification

The system calculates a matching score for each available asset and displays the resulting ranking in a graphical interface.

The project combines a simple knowledge base with weighted rules and partial matching to demonstrate how domain-specific knowledge can be represented and used for decision support.

## Features

- Weighted evaluation of financial assets
- Support for multiple asset classes:
  - Stocks
  - Bonds
  - Currencies
  - Cryptocurrencies
  - Futures
  - Options
  - Real estate funds
- Matching based on qualitative and quantitative criteria
- Partial matching for asset type and numerical parameters
- Investor qualification constraints
- Interactive desktop GUI built with PyQt6
- JSON-based financial asset knowledge base

## Architecture

The application follows a simple separation between the expert-system logic, data, and user interface:

```text
                    ┌──────────────────┐
                    │   PyQt6 GUI      │
                    │  MainWindow      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  ExpertSystem    │
                    │                  │
                    │ Weighted Rules   │
                    │ Matching Logic   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Knowledge Base │
                    │    assets.json   │
                    └──────────────────┘
```

### Main components

**`app/core/expert_system.py`**

Contains the expert-system logic. It loads the knowledge base, applies the evaluation rules, calculates weighted matching scores, and produces the ranked list of assets.

**`app/data/assets.json`**

Contains the financial asset knowledge base. Each asset is described by its market, risk level, asset type, parameter, liquidity, investment horizon, and investor qualification requirement.

**`app/ui/main_window.py`**

Implements the PyQt6 graphical interface and connects user input with the expert-system engine.

**`app/main.py`**

Application entry point.

## Evaluation Model

Each criterion has an associated weight:

| Criterion | Weight |
|---|---:|
| Asset type | 0.30 |
| Risk | 0.20 |
| Market | 0.20 |
| Investment horizon | 0.10 |
| Investor qualification | 0.10 |
| Parameter | 0.06 |
| Liquidity | 0.04 |

The system calculates an individual score for every asset based on the selected criteria.

Some criteria are evaluated as exact matches, while others allow partial matching. For example, asset-type compatibility is represented through a predefined compatibility matrix, while numerical parameters are evaluated according to the distance between the user's target value and the asset's value.

The final result is presented as a percentage relative to the maximum score achievable from the selected criteria.

## Example

The user can specify a combination of preferences such as:

```text
Market:              Moscow Exchange
Risk:                Low risk
Asset type:          Bond
Liquidity:           High
Investment horizon:  Long-term
```

The system then evaluates the available assets and displays them in descending order of their calculated matching score.

**Example of output**

|Number|Stock|Match %|
|-|-|-|
|1.|🟢 OFZ 26254 (Bond)|100|
|3.|🟢 Gazprom Neft (Bond)|100|
|2.|🟢 Sberbank PAO 001P-SBER52 (Bond)|95.7|
|4.|🟡 Modern 8 (REIT)|77.5|
|5.|🟡 Luzhniki Collection Moscow (REIT)|77.5|
|6.|🟡 LKOH (Stock)|67.3|

## Technologies

- Python
- PyQt6
- JSON
- Object-oriented programming
- Rule-based expert systems
- Weighted decision-making

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/Fuzzy-Asset-Selector.git
cd Fuzzy-Asset-Selector
```

Create virtual environment and install dependencies:

```bash
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python app/main.py
```

## Project Context

This project was developed as part of a university laboratory assignment focused on expert systems and their application to a financial domain.

The project provided practical experience with:

- modelling domain-specific knowledge;
- designing rule-based decision systems;
- implementing weighted criteria and partial matching;
- working with financial asset characteristics;
- developing a desktop interface for an expert system.

The financial data included in the project is intended for educational purposes and should not be considered investment advice.

## Possible Future Improvements

Potential extensions include:

- separating the knowledge base from the evaluation rules;
- introducing a more formal fuzzy inference model;
- improving the asset compatibility model;
- adding more financial instruments and characteristics;
- providing explanations for individual recommendations;
- adding tests for the expert-system rules;
- improving the architecture and configuration management.
