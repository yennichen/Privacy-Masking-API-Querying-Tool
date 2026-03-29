🛡️ Privacy Masking & Multi-Chain API Querying Tool
A professional OSINT utility for Web3 analysts to automate data masking, evidence collection, and multi-chain address screening.

🌟 Overview
This tool is designed to solve two major pain points in crypto investigations:

Privacy Masking: Automatically blurs PII (Emails, Internal IDs) on webpages before taking screenshots.

Instant Radar: Automatically checks if a crypto address has historical transactions across 20+ tokens (BTC, ETH, TRC20, SOL, etc.) the moment you capture the data.

🚀 Features
One-Click Masking: Uses a Chrome Extension to mosaic sensitive text via DOM manipulation.

Smart Naming: Automatically saves screenshots with standardized filenames based on internal entity mapping.

Multi-Chain Support: - EVM & L2s: via Moralis API.

Tron (TRC20): via TronGrid API.

UTXO (BTC/LTC): via Mempool/Litecoinspace public nodes.

Solana: via official Public RPC nodes.

Background Processing: History checks run in the background without slowing down your investigative workflow.

🛠️ Setup & Installation
Prerequisites
Python 3.10+

Google Chrome Browser

Installation
Clone the repository:

Bash
git clone https://github.com/yennichen/Privacy-Masking-API-Querying-Tool.git
cd Privacy-Masking-API-Querying-Tool
Install dependencies:

Bash
pip install -r requirements.txt
Configure your API Keys in AutoMask_API.py:

MORALIS_API_KEY

TRONGRID_API_KEY

Load the Extension:

Open Chrome chrome://extensions/

Enable "Developer mode".

Click "Load unpacked" and select the AutoMask_Extension folder.

⌨️ How to Use
Run the script:

Bash
python AutoMask_API.py
Press Win + W (or Alt + W) to start the recording sequence.

Copy URL -> Address -> Token (Ctrl+C for each).

Click the Chrome Extension icon on the target page to mask and capture.

Check your terminal for the On-chain Radar Analysis.