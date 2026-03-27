def suggestion_class(value: str) -> str:
    if value == "買入":
        return "tag-buy"
    if value == "持有":
        return "tag-hold"
    if value == "賣出":
        return "tag-sell"
    return "tag-default"