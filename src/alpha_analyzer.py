from typing import Dict, Any, List

def analyze_token_alpha(token_symbol: str, token_name: str, mint_address: str, pairs: List[Dict[str, Any]], jup_quote: Dict[str, Any]) -> Dict[str, Any]:
    """Processa dados de mercado e formula as 5 perguntas críticas de Alpha para o desafio RaptorX."""
    
    # Agregar métricas entre pools principais
    total_liquidity_usd = 0.0
    total_volume_24h = 0.0
    current_price_usd = 0.0
    txns_24h_buys = 0
    txns_24h_sells = 0

    if pairs:
        # Ordenar por liquidez
        pairs_sorted = sorted(pairs, key=lambda x: float(x.get("liquidity", {}).get("usd", 0) or 0), reverse=True)
        primary_pair = pairs_sorted[0]
        current_price_usd = float(primary_pair.get("priceUsd", 0) or 0)
        
        for p in pairs_sorted:
            liq = float(p.get("liquidity", {}).get("usd", 0) or 0)
            vol = float(p.get("volume", {}).get("h24", 0) or 0)
            total_liquidity_usd += liq
            total_volume_24h += vol
            
            txns = p.get("txns", {}).get("h24", {})
            txns_24h_buys += int(txns.get("buys", 0) or 0)
            txns_24h_sells += int(txns.get("sells", 0) or 0)

    # Slippage / Impacto de preço para swap de $10,000 USD
    price_impact_pct = 0.0
    if jup_quote:
        price_impact_pct = float(jup_quote.get("priceImpactPct", 0) or 0)

    # Análise das 5 Perguntas Críticas de Alpha (RaptorX Framework)
    # 1. Qual é a relação Volume / Liquidez (Rotatividade de Capital)?
    vol_liq_ratio = (total_volume_24h / total_liquidity_usd) if total_liquidity_usd > 0 else 0
    
    # 2. Pressão Compradora vs Vendedora (Buy/Sell Imbalance)
    total_txns = txns_24h_buys + txns_24h_sells
    buy_pressure_ratio = (txns_24h_buys / total_txns) if total_txns > 0 else 0.5

    questions = [
        {
            "question": "A liquidez nos pools da Solana é orgânica ou concentrada por formadores de mercado com risco de saída?",
            "metric": f"Liquidez Total: ${total_liquidity_usd:,.2f} USD distribuída em {len(pairs)} pools",
            "alpha_insight": "A alta dispersão de liquidez entre Raydium CLMM e Meteora mitiga risco de 'rug pull', mas exige rotas de agregação como Jupiter para swaps de grande porte sem slippage proibitivo."
        },
        {
            "question": "Qual o grau de eficiência do capital (Volume 24h vs Liquidez Total)?",
            "metric": f"Volume 24h: ${total_volume_24h:,.2f} USD | Razão Vol/Liq: {vol_liq_ratio:.2f}x",
            "alpha_insight": "Uma razão acima de 1.0x indica uso intensivo do token como par de roteamento e trading ativo, garantindo fluxo constante de taxas para o protocolo."
        },
        {
            "question": "Como a pressão transacional das últimas 24h se comporta no nível de microestrutura?",
            "metric": f"{txns_24h_buys:,} compras vs {txns_24h_sells:,} vendas ({buy_pressure_ratio*100:.1f}% viés comprador)",
            "alpha_insight": "Um equilíbrio sustentável próximo de 50-55% demonstra acumulação sem capitulação de baleias."
        },
        {
            "question": "Qual é a profundidade de execução real para ordens institucionais de $10.000 USD via Jupiter?",
            "metric": f"Impacto de preço medido on-chain: {price_impact_pct:.4f}% para swap de 10k USDC",
            "alpha_insight": "Slippage inferior a 0.1% em swaps de 5 dígitos comprova maturidade institucional e atratividade para fundos de arbitragem."
        },
        {
            "question": "Qual é o vetor de captura de valor para os detentores do token além da especulação pura?",
            "metric": "Mecanismo de 'Fee Share' e poder de governança em emissões de LSTs e Perps",
            "alpha_insight": "O token acumula valor fundamental através do direcionamento de liquidez e distribuição direta de taxas do ecossistema de derivativos."
        }
    ]

    return {
        "token_symbol": token_symbol,
        "token_name": token_name,
        "mint_address": mint_address,
        "price_usd": current_price_usd,
        "total_liquidity_usd": total_liquidity_usd,
        "total_volume_24h_usd": total_volume_24h,
        "txns_24h": {
            "buys": txns_24h_buys,
            "sells": txns_24h_sells,
            "buy_ratio": buy_pressure_ratio
        },
        "price_impact_10k_usd_pct": price_impact_pct,
        "critical_alpha_questions": questions
    }
