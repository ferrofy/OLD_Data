# 🔗 FerroFy New Smart Contracts

> **Deployed On:** Sepolia Testnet | **Chain ID:** 11155111
> **Deployer:** `0x91b2Aef20c29d87d8dcc48191b30FbC1562aAaF0`

---

## 📋 Contract Overview

| # | Contract | Symbol | Decimals | Initial Supply | Address |
|---|----------|--------|----------|---------------|---------|
| 1 | FerroFy Indian Rupee | **INRf** | 2 | 1,000,000,000 | `0x594780D36EDb851B54ADBFefeC30D5Bb6BF0008E` |
| 2 | Temperature | **TEMP** | 2 | 1,000,000,000 | `0x6b383C9AE7DE29023dE6c836317058993E9A3B30` |
| 3 | Humidity | **HUM** | 2 | 1,000,000,000 | `0xe6b5076C555A1067c6bC5152E475C9dA74A54b1B` |
| 4 | Smoke | **MQ2** | 2 | 1,000,000,000 | `0x793b9c17eA4527412EA6d66d0bd02A78dc41e13f` |
| 5 | Rain | **RAIN** | 2 | 1,000,000,000 | `0x7c48c5a7284aE2EeA4d1e7d89c79005E6ccf845d` |
| 6 | Sensor Storage | — | — | — | `0xCc19060642C8fb3A090ff7e69740d93D8773B190` |

---

## 💡 How Sensor-Linked Token Transfers Work

Each sensor token reward minted is **equal to the sensor reading value** (in centi-units, 2 decimal precision).

| Sensor | Reading Example | Amount Stored | Tokens Minted |
|--------|----------------|--------------|--------------|
| Temperature | 30.55 °C | `3055` (centi) | 30.55 TEMP |
| Humidity | 10% | `1000` (centi) | 10.00 HUM |
| Smoke (MQ2) | 512.75 | `51275` (centi) | 512.75 MQ2 |
| Rain | 200.50 | `20050` (centi) | 200.50 RAIN |

> **All values use 2 decimal precision.** Multiply real-world value × 100 before sending to the contract.

---

## 💳 Payment Token

- **Only INRf is used** for upload and fetch fees
- No PyUSD or TestnetUSD
- Upload Fee: **0.50 INRf**
- Fetch Fee: **0.25 INRf**

---

## 📁 New Files Created

```
Contracts/
  INRf/
    INRf_Token.sol       ← New INRf (1B supply, 2 decimals, mintable+burnable)
  Sensor/
    SensorTokenBase.sol  ← Base for all sensor tokens
    TEMP_Token.sol       ← Temperature token (TEMP)
    HUM_Token.sol        ← Humidity token (HUM)
    MQ2_Token.sol        ← Smoke token (MQ2)
    RAIN_Token.sol       ← Rain token (RAIN)
  Storage/
    Data.sol             ← Rebuilt: INRf-only, centi-unit readings, sensor-proportional rewards

scripts/
  Deploy_New.js          ← New deployment script

New_Contracts.json       ← Deployed contract addresses
```

---

## 🔐 Etherscan Links (Sepolia)

| Contract | Sepolia Etherscan |
|----------|------------------|
| INRf | [View](https://sepolia.etherscan.io/address/0x594780D36EDb851B54ADBFefeC30D5Bb6BF0008E) |
| TEMP | [View](https://sepolia.etherscan.io/address/0x6b383C9AE7DE29023dE6c836317058993E9A3B30) |
| HUM | [View](https://sepolia.etherscan.io/address/0xe6b5076C555A1067c6bC5152E475C9dA74A54b1B) |
| MQ2 | [View](https://sepolia.etherscan.io/address/0x793b9c17eA4527412EA6d66d0bd02A78dc41e13f) |
| RAIN | [View](https://sepolia.etherscan.io/address/0x7c48c5a7284aE2EeA4d1e7d89c79005E6ccf845d) |
| Sensor Storage | [View](https://sepolia.etherscan.io/address/0xCc19060642C8fb3A090ff7e69740d93D8773B190) |
