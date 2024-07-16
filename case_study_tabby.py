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

# Тест-кейсы

# [1][SC_B] Triggers (score <= 400)
input_data_1 = {
    "id": "6438Tty_4ff00278",
    "score": 350,
    "items": "iphone",
    "amount": 100,
    "registered_since_at_store": "2024-06-03",
    "ApplicationDate": "2024-07-03",
    "score_v2": 300,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_1 = decision_making_system(input_data_1)
print("[1][SC_B]:")
print(json.dumps(result_1, indent=4))

# [2][SC_B] Triggers (items and amount)
input_data_2 = {
    "id": "6438Tty_4ff00278",
    "score": 450,
    "items": "iphone, galaxy",
    "amount": 250,
    "registered_since_at_store": "2024-01-01",
    "ApplicationDate": "2024-07-03",
    "score_v2": 300,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_2 = decision_making_system(input_data_2)
print("\n[2][SC_B]:")
print(json.dumps(result_2, indent=4))

# [3][SC_B] Triggers (registration date)
input_data_3 = {
    "id": "6438Tty_4ff00278",
    "score": 520,
    "items": "tv",
    "amount": 250,
    "registered_since_at_store": "2024-06-15",
    "ApplicationDate": "2024-07-03",
    "score_v2": 300,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_3 = decision_making_system(input_data_3)
print("\n[3][SC_B]:")
print(json.dumps(result_3, indent=4))

# [4][SC_B] Triggers (score_v2)
input_data_4 = {
    "id": "6438Tty_4ff00278",
    "score": 600,
    "items": "tv",
    "amount": 100,
    "registered_since_at_store": "2024-01-01",
    "ApplicationDate": "2024-07-03",
    "score_v2": 200,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_4 = decision_making_system(input_data_4)
print("\n[4][SC_B]:")
print(json.dumps(result_4, indent=4))

# [5][SC_B] SC_B exception
input_data_5 = {
    "id": "6438Tty_4ff00278",
    "score": 350,
    "items": "iphone",
    "amount": 100,
    "registered_since_at_store": "2024-06-03",
    "ApplicationDate": "2024-07-03",
    "score_v2": 300,
    "risk_strategy_type": "light",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_5 = decision_making_system(input_data_5)
print("\n[5][SC_B]:")
print(json.dumps(result_5, indent=4))

# [1][SC_N] Triggers (score <= 350)
input_data_6 = {
    "group_id": "6ef811855e53",
    "item": "video",
    "score": 300,
    "amount": 500,
    "identity_score": 50,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_6 = decision_making_system(input_data_6)
print("\n[1][SC_N]:")
print(json.dumps(result_6, indent=4))

# [2][SC_N] Triggers (amount condition)
input_data_7 = {
    "group_id": "6ef811855e53",
    "item": "camera",
    "score": 380,
    "amount": 700,
    "identity_score": 50,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_7 = decision_making_system(input_data_7)
print("\n[2][SC_N]:")
print(json.dumps(result_7, indent=4))

# [3][SC_N] Triggers (identity_score)
input_data_8 = {
    "group_id": "6ef811855e53",
    "item": "kitchen_dining",
    "score": 410,
    "amount": 800,
    "identity_score": 110,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_8 = decision_making_system(input_data_8)
print("\n[3][SC_N]:")
print(json.dumps(result_8, indent=4))

# [4][SC_N] SC_N exception
input_data_9 = {
    "group_id": "6ef811855e53",
    "item": "video",
    "score": 300,
    "amount": 500,
    "identity_score": 50,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "installments"
}

result_9 = decision_making_system(input_data_9)
print("\n[4][SC_N]:")
print(json.dumps(result_9, indent=4))

# [1][SC_B][SC_N] No rules trigger (approve)
input_data_10 = {
    "id": "different_id",
    "group_id": "different_group",
    "score": 600,
    "items": "book",
    "amount": 50,
    "registered_since_at_store": "2024-01-01",
    "ApplicationDate": "2024-07-03",
    "score_v2": 300,
    "identity_score": 50,
    "risk_strategy_type": "high",
    "payment_is_test": "false",
    "product_type": "standard"
}

result_10 = decision_making_system(input_data_10)
print("\n[1][SC_B][SC_N]:")
print(json.dumps(result_10, indent=4))
