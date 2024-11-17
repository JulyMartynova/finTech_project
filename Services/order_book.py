from collections import deque
from flask import Flask
import datetime
from db import db
from prettytable import PrettyTable
from web3 import Web3
from models import transaction, order
from Services.wallet_service import get_wallet

class OrderBook:
    def __init__(self):
        self.buy_orders = deque()
        self.sell_orders = deque()

    def add_order(self, order):
        try:
            if order.type not in ['buy', 'sell']:
                raise ValueError("Invalid order type. Must be 'buy' or 'sell'")
            if not isinstance(order.price, (int, float)) or order.price <= 0:
                raise ValueError("Negative order price. It must be positive.")
            if not isinstance(order.quantity, (int, float)) or order.quantity <= 0:
                raise ValueError("Negative order quantity. It must be positive.")

            wallet = get_wallet(order.user_id, order.wallet_id)

            if order.type == 'buy' and wallet.balance < order.price * order.quantity:
                raise ValueError("Insufficient funds in the wallet")

            if order.type == 'buy':
                self.buy_orders.append(order)
            else:
                self.sell_orders.append(order)

        except KeyError as e:
            print(f'KeyError: Missing key in order dictionary: {e}')
        except ValueError as e:
            print(f'ValueError: {e}')
        except Exception as e:
            print(f'Error occurred: {e}')

    def matching_engine(self):
        while self.buy_orders and self.sell_orders:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]

            if buy_order.price >= sell_order.price:
                total_quantity_buy = sum(order.quantity for order in self.buy_orders)
                total_quantity_sell = sum(order.quantity for order in self.sell_orders)

                for buy_order in self.buy_orders:
                    for sell_order in self.sell_orders:
                        if buy_order.price >= sell_order.price:
                            total_trade_quantity = min(buy_order.quantity, sell_order.quantity)
                            total_trade_quantity = min(total_trade_quantity, total_quantity_buy * (sell_order.quantity / total_quantity_sell))

                            transaction = transaction(
                                buyer_id=buy_order.user_id,
                                seller_id=sell_order.user_id,
                                price=sell_order.price,
                                quantity=total_trade_quantity,
                                created_at=datetime.datetime.utcnow()
                            )
                            if self.send_transaction(transaction):
                                buy_order.quantity -= total_trade_quantity
                                sell_order.quantity -= total_trade_quantity

                                if buy_order.quantity == 0:
                                    self.buy_orders.remove(buy_order)

                                if sell_order.quantity == 0:
                                    self.sell_orders.remove(sell_order)
                                else:
                                    break

            else:
                break

    def send_transaction(self, transaction):
        buyer_wallet = get_wallet(transaction.buyer_id, transaction.buyer_wallet_id)
        seller_wallet = get_wallet(transaction.seller_id, transaction.seller_wallet_id)

        if buyer_wallet and seller_wallet and not buyer_wallet.is_cold and not seller_wallet.is_cold:
            w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f13b5c02ca9945768aa5c1749957a6e7'))
            tx_hash = w3.eth.send_transaction({
                'to': seller_wallet.address,
                'value': w3.toWei(transaction.price * transaction.quantity, 'ether'),
                'gas': 21000,
                'gasPrice': w3.toWei('50', 'gwei'),
                'nonce': w3.eth.getTransactionCount(buyer_wallet.address),
            })

            self.write_transaction_to_timescale(transaction)
            
            return True
        return False

    def write_transaction_to_timescale(self, transaction):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        engine = create_engine('postgresql+psycopg2://username:password@localhost/your_database')
        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(transaction)
        session.commit()

    def get_order_book(self): 
        table = PrettyTable()
        table.field_names = ["Type", "Price", "Quantity", "User ID", "Date"]

        for order in self.buy_orders:
            table.add_row(["Buy", order.price, order.quantity, order.user_id, order.created_at])
        for order in self.sell_orders:
            table.add_row(["Sell", order.price, order.quantity, order.user_id, order.created_at])
        
        return table

def init_order_book(app):
    global order_book
    order_book = OrderBook()