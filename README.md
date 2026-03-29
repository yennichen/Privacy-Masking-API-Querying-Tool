# 🛡️ Privacy Masking & Multi-Chain API Querying Tool

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Web3](https://img.shields.io/badge/Web3-Intelligence-orange?style=for-the-badge)

An advanced, automated OSINT utility designed for **Web3 Intelligence Analysts**. This tool streamlines the process of capturing evidence while ensuring operational security (OPSEC) through automated data masking and real-time on-chain history screening.

---

## 🌟 Overview

Investigating crypto crimes often requires capturing dozens of screenshots while cross-referencing multiple blockchains. This tool eliminates the manual grind:

* **⚡ Instant OPSEC:** Automatically blurs sensitive PII (Emails, IDs) before you hit capture.
* **📡 Smart Radar:** Does the "boring work" of checking 20+ tokens' history across 5+ different API/Node providers in the background.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **1-Click Masking** | Uses a Chrome Extension to mosaic sensitive text via real-time DOM manipulation. |
| **Smart Naming** | Auto-saves screenshots with standardized filenames: `Entity_Token_Address.png`. |
| **Multi-Chain Radar** | Background API routing to check if an address is active or a "fresh" burner. |
| **Taskbar Filtering** | Automatically crops the OS taskbar for clean, report-ready forensic evidence. |

---

## ⛓️ Supported Chains & Methods

| Ecosystem | Tokens Supported | Provider |
| :--- | :--- | :--- |
| **EVM & L2s** | ETH, BSC, Polygon, AVAX, ARB, OP | **Moralis API** |
| **Tron** | TRX, USDT-TRC20 | **TronGrid API** |
| **UTXO** | BTC, LTC | **Mempool / Litecoinspace** |
| **Solana** | SOL | **Official Public RPC** |
| **TON** | TON | **TonAPI** |

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* **Python 3.10+**
* **Google Chrome Browser**

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/yennichen/Privacy-Masking-API-Querying-Tool.git](https://github.com/yennichen/Privacy-Masking-API-Querying-Tool.git)

# Enter the directory
cd Privacy-Masking-API-Querying-Tool

# Install dependencies
pip install -r requirements.txt

```

### 3. Configuration
Open AutoMask_API.py and input your keys:

### 4. Operational Workflow
1. Launch: Run python AutoMask_API.py.
2. Trigger: Press Win + W (or Alt + W) to start the sequence.
3. Capture Data: Copy URL ➔ Address ➔ Token (Ctrl+C for each).
4. Execute: Click the Extension Icon in Chrome to mask and capture.
5. Analyze: Review the On-chain Radar results in your terminal instantly.

### 5. Disclaimer
[!IMPORTANT]
This tool is developed for forensic investigation and educational purposes only. The author is not responsible for any misuse. Always ensure you have the proper authorization before conducting on-chain analysis.