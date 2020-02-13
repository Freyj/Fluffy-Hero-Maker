class PFItem:
    """
        Class representing an item in Pathfinder (1e)
    """
    def __init__(self, name: str):
        self.name = name
        self.type = None
        self.sub_type = None
        # price stored in gold pieces
        self.buy_price = 0
        self.sell_price = 0
        # weight in kg
        self.weight = 0
        self.description = None
        self.special = None

    def cli_display_string(self):
        result_str = "Name: {name}\nType: {type}".format(name=self.name, type=self.type)
        if self.sub_type is not None:
            result_str += "\nSubtype: {subtype}".format(subtype=self.sub_type)
        result_str += "\nBuy Price: {buyp}\nSell Price: {sellp}".format(buyp=self.buy_price, sellp=self.sell_price)
        if self.weight > 0:
            result_str += "\nWeight: {weight}kg".format(weight=self.weight)
        result_str += "\nDescription: {desc}".format(desc=self.description)
        if self.special is not None:
            result_str += "\nSpecial: {spc}".format(spc=self.special)
        return result_str
