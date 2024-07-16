import json
from datetime import datetime

def check_rule_SC_B(data):
    id_match = data.get("id") == "6438Tty_4ff00278"
    score = data.get("score", float('inf'))
    items = data.get("items", "")
    amount = data.get("amount", 0)
    registered_since = data.get("registered_since_at_store")
    application_date = data.get("ApplicationDate")
    score_v2 = data.get("score_v2", float('inf'))
    risk_strategy_type = data.get("risk_strategy_type", "")
    payment_is_test = data.get("payment_is_test", "false")
    product_type = data.get("product_type", "")
    #rule
    if id_match and (
        score <= 400 or
        (score <= 500 and any(item in items for item in ["iphone", "galaxy", "redmi", "poco"]) and amount > 200) or
        (score <= 550 and (datetime.strptime(application_date, "%Y-%m-%d") - datetime.strptime(registered_since, "%Y-%m-%d")).days <= 30 and amount > 200) or
        score_v2 <= 250
    ):
        if risk_strategy_type in ['light', 'middle'] or payment_is_test == "true" or product_type == 'card_installments':
            return {"decision": "", "stop_factors": "SC_B;"}
        else:
            return {"decision": "reject", "stop_factors": "SC_B;"}
    return None

def check_rule_SC_N(data):
    group_id_match = data.get("group_id") == "6ef811855e53"
    item = data.get("item", "")
    score = data.get("score", float('inf'))
    amount = data.get("amount", 0)
    identity_score = data.get("identity_score", float('-inf'))
    risk_strategy_type = data.get("risk_strategy_type", "")
    payment_is_test = data.get("payment_is_test", "false")
    product_type = data.get("product_type", "")

    if group_id_match and item in ["video", "camera", "kitchen_dining", "bath", "baby_product"] and (
        score <= 350 or
        (score <= 400 and amount > 600) or
        (score <= 420 and amount > 1200) or
        (identity_score > 100 and amount > 750 and score <= 420)
    ):
        if risk_strategy_type in ['light', 'middle'] or payment_is_test == "true" or product_type == 'installments':
            return {"decision": "", "stop_factors": "SC_N;"}
        else:
            return {"decision": "reject", "stop_factors": "SC_N;"}
    return None

def decision_making_system(data):
    result_SC_B = check_rule_SC_B(data)
    if result_SC_B:
        return result_SC_B

    result_SC_N = check_rule_SC_N(data)
    if result_SC_N:
        return result_SC_N

    return {"decision": "approve", "stop_factors": ""}

# Пример использования
input_data = {
  "id": "6438Tty_4ff00278",
  "score": 600,
  "items": "iphone",
  "amount": 100,
  "registered_since_at_store": "2023-01-01",
  "ApplicationDate": "2023-07-01",
  "score_v2": 300,
  "risk_strategy_type": "high",
  "payment_is_test": "false",
  "product_type": "loan"
}

result = decision_making_system(input_data)
print(json.dumps(result, indent=4))
