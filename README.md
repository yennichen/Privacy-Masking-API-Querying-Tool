# 🛡️ Web3 Intelligence AutoMask & Radar Tracker

A professional OSINT utility for Web3 analysts to automate data masking, evidence collection, and multi-chain address screening.

## 🌟 Overview
This tool is designed to solve two major pain points in crypto investigations:
1. **Privacy Masking:** Automatically blurs PII (Emails, Internal IDs) on webpages before taking screenshots.
2. **Instant Radar:** Automatically checks if a crypto address has historical transactions across 20+ tokens (BTC, ETH, TRC20, SOL, etc.) the moment you capture the data.

## 🚀 Features
- **One-Click Masking:** Uses a Chrome Extension to mosaic sensitive text via DOM manipulation.
- **Smart Naming:** Automatically saves screenshots with standardized filenames based on entity mapping.
- **Multi-Chain Support:** - **EVM & L2s:** via Moralis API.
    - **Tron (TRC20):** via TronGrid API.
    - **UTXO (BTC/LTC):** via Mempool/Litecoinspace public nodes.
    - **Solana:** via official Public RPC.
- **Background Processing:** History checks run asynchronously without slowing down your workflow.

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Google Chrome Browser

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/Chainlabs-AutoMask-Radar.git](https://github.com/YourUsername/Chainlabs-AutoMask-Radar.git)
   cd Chainlabs-AutoMask-Radar