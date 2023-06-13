
def get_items_to_trade(trade_items, profile):
    user_trade_items = []
    for trade_item in trade_items:
        items = profile.useritem_set.filter(item=trade_item.item)
        if items:
            for item in items:
                if item not in user_trade_items:
                    user_trade_items.append(item)
                    break
            else:
                return []
        else:
            return []
        
    return user_trade_items