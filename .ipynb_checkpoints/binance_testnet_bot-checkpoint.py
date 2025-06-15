import logging
from binance.client import Client
from binance.enums import *
import os

# Setup logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.testnet = testnet
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            logging.info("Connected to Binance Futures Testnet")
        else:
            logging.info("Connected to Binance Futures Mainnet")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == ORDER_TYPE_MARKET:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            elif order_type == ORDER_TYPE_LIMIT:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price,
                    timeInForce=TIME_IN_FORCE_GTC
                )
            else:
                logging.error(f"Unsupported order type: {order_type}")
                return None

            logging.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")
            print(f"Error placing order: {e}")
            return None


def main():
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        print("Please set your BINANCE_API_KEY and BINANCE_API_SECRET as environment variables.")
        return

    bot = BasicBot(api_key, api_secret, testnet=True)

    while True:
        try:
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            order_type = input("Enter order type (MARKET/LIMIT): ").upper()
            quantity = float(input("Enter quantity: "))
            price = None
            if order_type == "LIMIT":
                price = float(input("Enter price: "))

            order = bot.place_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                order_type=ORDER_TYPE_MARKET if order_type == "MARKET" else ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price
            )

            if order:
                print(f"Order executed: {order['orderId']}")
            else:
                print("Order failed. Check bot.log for details.")


        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            print("Error occurred. Check logs.")


if __name__ == "__main__":
    main()
