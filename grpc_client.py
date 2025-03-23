import grpc
import logging
import argparse

# Import the generated classes
import currency_pb2
import currency_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)


class CurrencyClient:
    """Client for gRPC Currency Converter service."""

    def __init__(self, host='localhost', port=50051):
        """Initialize client with server address."""
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = currency_pb2_grpc.CurrencyConverterStub(self.channel)
        logging.info(f"Client initialized, connecting to {host}:{port}")

    def convert(self, from_currency, to_currency, amount):
        """Convert currency."""
        try:
            request = currency_pb2.ConversionRequest(
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount
            )
            response = self.stub.Convert(request)
            
            if response.success:
                logging.info(f"Conversion successful: {amount} {response.from_currency} = "
                           f"{response.converted_amount} {response.to_currency} "
                           f"(rate: {response.exchange_rate})")
                return response
            else:
                logging.error(f"Conversion failed: {response.error_message}")
                return None
        except grpc.RpcError as e:
            logging.error(f"RPC error: {e}")
            return None

    def get_exchange_rate(self, from_currency, to_currency):
        """Get exchange rate between two currencies."""
        try:
            request = currency_pb2.ExchangeRateRequest(
                from_currency=from_currency,
                to_currency=to_currency
            )
            response = self.stub.GetExchangeRate(request)
            
            if response.success:
                logging.info(f"Exchange rate: 1 {from_currency} = {response.exchange_rate} {to_currency}")
                return response.exchange_rate
            else:
                logging.error(f"Failed to get exchange rate: {response.error_message}")
                return None
        except grpc.RpcError as e:
            logging.error(f"RPC error: {e}")
            return None

    def get_available_currencies(self):
        """Get all available currencies."""
        try:
            request = currency_pb2.EmptyRequest()
            response = self.stub.GetAvailableCurrencies(request)
            
            if response.success:
                currencies = response.currencies
                logging.info(f"Available currencies ({len(currencies)}): {', '.join(currencies)}")
                return currencies
            else:
                logging.error(f"Failed to get currencies: {response.error_message}")
                return None
        except grpc.RpcError as e:
            logging.error(f"RPC error: {e}")
            return None

    def close(self):
        """Close the channel."""
        self.channel.close()


def run_interactive_client(host='localhost', port=50051):
    """Run an interactive client session."""
    client = CurrencyClient(host, port)
    
    print("\n=== Currency Converter Client ===")
    print("Available commands:")
    print("1. convert <from_currency> <to_currency> <amount>")
    print("2. rate <from_currency> <to_currency>")
    print("3. currencies")
    print("4. exit")
    
    while True:
        command = input("\nEnter command: ").strip().split()
        
        if not command:
            continue
            
        if command[0] == "exit":
            break
        
        elif command[0] == "convert":
            if len(command) != 4:
                print("Usage: convert <from_currency> <to_currency> <amount>")
                continue
                
            try:
                from_currency = command[1].upper()
                to_currency = command[2].upper()
                amount = float(command[3])
                result = client.convert(from_currency, to_currency, amount)
                
                if result:
                    print(f"\n{amount} {result.from_currency} = {result.converted_amount} {result.to_currency}")
                    print(f"Exchange rate: 1 {result.from_currency} = {result.exchange_rate} {result.to_currency}")
            except ValueError:
                print("Error: Amount must be a number")
        
        elif command[0] == "rate":
            if len(command) != 3:
                print("Usage: rate <from_currency> <to_currency>")
                continue
                
            from_currency = command[1].upper()
            to_currency = command[2].upper()
            rate = client.get_exchange_rate(from_currency, to_currency)
            
            if rate:
                print(f"\nExchange rate: 1 {from_currency} = {rate} {to_currency}")
        
        elif command[0] == "currencies":
            currencies = client.get_available_currencies()
            
            if currencies:
                print("\nAvailable currencies:")
                # Print in rows of 5
                for i in range(0, len(currencies), 5):
                    print("  " + "  ".join(currencies[i:i+5]))
        
        else:
            print("Unknown command. Available: convert, rate, currencies, exit")
    
    client.close()
    print("Client session ended.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Currency Converter Client')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=50051, help='Server port')
    
    args = parser.parse_args()
    run_interactive_client(args.host, args.port)