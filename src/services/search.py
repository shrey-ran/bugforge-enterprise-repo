"""Search and analytics service for the enterprise platform."""
import re
from collections import Counter

def search_products(query: str, products: list, max_results: int = 10) -> list:
    """Search products by name or description. Returns ranked results."""
    query_lower = query.lower()
    scored = []
    
    for product in products:
        score = 0
        name = product.get("name", "").lower()
        description = product.get("description", "").lower()
        
        # Exact match in name gets highest score
        if query_lower in name:
            score += 10
        # Partial word matches in name
        for word in query_lower.split():
            if word in name:
                score += 3
            if word in description:
                score += 1
        
        if score > 0:
            scored.append((score, product))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:max_results]]

def calculate_trending_score(views: int, purchases: int, days_listed: int) -> float:
    """Calculate a trending score for a product.
    
    Formula: (views * 0.3 + purchases * 0.7) / days_listed
    Higher score = more trending
    """
    if days_listed <= 0:
        return 0.0
    # BUG: Multiplied by days_listed instead of dividing.
    # Products listed longer get unfairly boosted instead of normalized.
    return (views * 0.3 + purchases * 0.7) * days_listed

def extract_keywords(text: str) -> list:
    """Extract meaningful keywords from text for indexing."""
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for", "of", "and", "or", "but", "with"}
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [w for w in words if w not in stop_words]

def generate_analytics_report(events: list) -> dict:
    """Generate an analytics summary from a list of events."""
    if not events:
        return {"total_events": 0, "top_actions": [], "unique_users": 0}
    
    actions = Counter(e.get("action") for e in events)
    users = set(e.get("user_id") for e in events)
    
    return {
        "total_events": len(events),
        "top_actions": actions.most_common(5),
        "unique_users": len(users)
    }
