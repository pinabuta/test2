class Rule:
    def __init__(self, name, condition, exception):
        self.name = name
        self.condition = condition
        self.exception = exception

def check(data):
    rules = [
        Rule("jope_rule", lambda x: "jopa" in x, lambda y: "exception" in data)
    ]

    result = {}
    for rule in rules:
        if rule.condition(data):
            result["stop_factors"] = rule.name
            result["decision"] = "" if rule.exception(data) else "rejected"
            break

    if "decision" not in result:
        result["decision"] = "approved"

    return result


first_check = check({"jopa": True, "exception": True})
print("Result: ", first_check)

