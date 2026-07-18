# utils/currency.py

def get_currency_info(state_or_country):
    """
    Returns the currency code, symbol, and approximate conversion rate from INR
    for a given state or country name.
    """
    if not state_or_country:
        return {'code': 'INR', 'symbol': '₹', 'rate': 1.0}
        
    loc = state_or_country.lower()
    
    # Define mapping of region/country keywords to currencies
    # Rates are approximate: 1 INR = X Foreign Currency
    currencies = [
        # Europe
        (['europe', 'france', 'germany', 'italy', 'spain', 'netherlands', 'belgium', 'greece', 'portugal'], 
         {'code': 'EUR', 'symbol': '€', 'rate': 0.011}),
        
        # UK
        (['uk', 'united kingdom', 'england', 'scotland', 'wales', 'london'], 
         {'code': 'GBP', 'symbol': '£', 'rate': 0.0094}),
         
        # USA
        (['usa', 'united states', 'america', 'new york', 'california'], 
         {'code': 'USD', 'symbol': '$', 'rate': 0.012}),
         
        # UAE
        (['uae', 'dubai', 'abu dhabi', 'united arab emirates'], 
         {'code': 'AED', 'symbol': 'د.إ', 'rate': 0.044}),
         
        # Singapore
        (['singapore'], 
         {'code': 'SGD', 'symbol': 'S$', 'rate': 0.016}),
         
        # Thailand
        (['thailand', 'bangkok', 'phuket'], 
         {'code': 'THB', 'symbol': '฿', 'rate': 0.43}),
         
        # Japan
        (['japan', 'tokyo', 'kyoto', 'osaka'], 
         {'code': 'JPY', 'symbol': '¥', 'rate': 1.75}),
         
        # Australia
        (['australia', 'sydney', 'melbourne'], 
         {'code': 'AUD', 'symbol': 'A$', 'rate': 0.018}),
         
        # Canada
        (['canada', 'toronto', 'vancouver'], 
         {'code': 'CAD', 'symbol': 'C$', 'rate': 0.016}),
         
        # Malaysia
        (['malaysia', 'kuala lumpur'], 
         {'code': 'MYR', 'symbol': 'RM', 'rate': 0.057}),
         
        # Switzerland
        (['switzerland', 'zurich', 'geneva'], 
         {'code': 'CHF', 'symbol': 'CHF', 'rate': 0.011}),
    ]
    
    for keywords, info in currencies:
        if any(keyword in loc for keyword in keywords):
            return info
            
    # Default to INR for Indian states or unknown locations
    return {'code': 'INR', 'symbol': '₹', 'rate': 1.0}

def get_rate_for_currency(currency_code):
    """
    Returns the conversion rate from INR to the given currency code.
    If the currency is USD, rate = ~0.012 (meaning 1 INR = 0.012 USD).
    To convert USD to INR, do: usd_amount / rate
    """
    if currency_code == 'INR':
        return 1.0
        
    currencies = [
        {'code': 'EUR', 'rate': 0.011},
        {'code': 'GBP', 'rate': 0.0094},
        {'code': 'USD', 'rate': 0.012},
        {'code': 'AED', 'rate': 0.044},
        {'code': 'SGD', 'rate': 0.016},
        {'code': 'THB', 'rate': 0.43},
        {'code': 'JPY', 'rate': 1.75},
        {'code': 'AUD', 'rate': 0.018},
        {'code': 'CAD', 'rate': 0.016},
        {'code': 'MYR', 'rate': 0.057},
        {'code': 'CHF', 'rate': 0.011},
    ]
    
    for info in currencies:
        if info['code'] == currency_code:
            return info['rate']
            
    return 1.0
