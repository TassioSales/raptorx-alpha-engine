# RaptorX Alpha Engine: Ask Better Questions. Find Better Alpha.

Automated empirical on-chain token research and alpha formulation framework for the Solana ecosystem.

> **Superteam Earn Bounty Submission:** *RaptorX Research Challenge ($125 USDC)*  
> **Author:** Tassio Sales  
> **Platform:** [Superteam Earn](https://earn.superteam.fun/listings/bounties/raptorx-research-challenge-ask-better-questions-find-better-alpha)  
> **Sponsor:** RaptorX Labs  

---

## Overview

The **RaptorX Alpha Engine** queries live Solana DEX pools (Raydium, Orca, Meteora via DexScreener) and the **Jupiter V6 Routing API** to formulate high-conviction, data-backed questions on market microstructure, capital rotation, and liquidity resilience for leading Solana tokens:
- **Jupiter (`JUP`)**
- **Raydium (`RAY`)**

## Quick Start

```bash
pip install -r requirements.txt
python src/main.py
```

The engine generates:
1. `data/alpha_report.json`: Full raw API payload and calculated metrics.
2. `REPORT.md`: Comprehensive submission report answering the 5 critical research questions with live on-chain metrics.
