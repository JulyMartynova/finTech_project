from collections import deque
class Order_Book():
    def __init__(self):
        self.buy_orders = deque()
        self.sell_orders = deque()
    def __add__(self, order): 
        try:
            if order['type'] not in ['buy', 'sell']:
                raise ValueError("Invalid order type. Must be buy or sell")
            if not isinstance(order['price'], (int, float)) or order['price'] <= 0:
                raise ValueError("Negative order price. It must be positive.")
            if not isinstance(order['quantity'],(int, float)) or order['quantity'] <= 0:
                raise ValueError("Negative order quantity. It must be positive.")
            if order['type'] == 'buy':
                self.buy_orders.append(order)
            else :
                self.sell_orders.append(order)
        except KeyError as e:
            print(f'KeyError: Missing key in order dictionary: {e}')
        except ValueError as e:
            print(f'ValueError: Missing key in order dictionary: {e}')
        except Exception as e:
            print(f'Error occured {e}')
    def __matching__engine__(self):
        total_trade_quantity, total_quantity_buy, total_quantity_sell = 0,0,0
        while self.buy_orders and self.sell_orders:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]

            if buy_order['price'] >= sell_order['price']:
                total_quantity_buy = sum(order['quantity'] for order in self.buy_orders)
                total_quantity_sell = sum(order['quantity'] for order in self.sell_orders)
            for buy_order in self.buy_orders:
                for sell_order in self.sell_orders:
                    if buy_order['price'] >= sell_order['price']:
                        total_trade_quantity = min(buy_order['quantity'], sell_order['quantity'])
                        total_trade_quantity = min(total_trade_quantity, total_quantity_buy * (sell_order['quantity']/ total_quantity_sell))
                    
                    buy_order['quantity'] -= total_trade_quantity
                    sell_order['quantity'] -= total_trade_quantity

                    if buy_order['quantity'] == 0: 
                        self.buy_orders.remove(buy_order)

                    if sell_order['quantity'] == 0:
                        self.sell_orders.remove(sell_order)
                    else:
                        break
    

                    




    
        