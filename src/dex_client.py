import requests
import time
from typing import Dict, Any, Optional, List

class SolanaTokenClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "RaptorX-Alpha-Researcher/1.0"})

    def get_token_pairs(self, token_address: str) -> List[Dict[str, Any]]:
        """Busca pares de liquidez e volume via DexScreener API."""
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json().get("pairs", [])
        except Exception as e:
            print(f"Erro ao consultar DexScreener: {e}")
        return []

    def get_jupiter_route(self, input_mint: str, output_mint: str, amount: int) -> Optional[Dict[str, Any]]:
        """Consulta cotação e impacto de preço (slippage / profundidade) via Jupiter API."""
        url = f"https://api.jup.ag/swap/v1/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps=50"
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None
