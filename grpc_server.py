import json
import time
import grpc
from concurrent import futures
import logging

# Import the generated classes
import currency_pb2
import currency_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)


class CurrencyConverterServicer(currency_pb2_grpc.CurrencyConverterServicer):
    """Implementation of CurrencyConverter service."""

    def __init__(self, exchange_rates_file):
        """Initialize the servicer with exchange rates data."""
        self.exchange_rates = self._load_exchange_rates(exchange_rates_file)
        self.last_loaded = time.time()
        self.reload_interval = 3600  # Reload rates every hour (in seconds)
        self.exchange_rates_file = exchange_rates_file
        logging.info(f"Loaded exchange rates from {exchange_rates_file}")
        logging.info(f"Available currencies: {', '.join(self.exchange_rates['rates'].keys())}")

    def _load_exchange_rates(self, file_path):
        """Load exchange rates from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"Error loading exchange rates: {e}")
            # Return a minimal default structure if file loading fails
            return {"base": "USD", "rates": {"USD": 1.0}}

    def _maybe_reload_rates(self):
        """Reload exchange rates if needed."""
        current_time = time.time()
        if current_time - self.last_loaded > self.reload_interval:
            self.exchange_rates = self._load_exchange_rates(self.exchange_rates_file)
            self.last_loaded = current_time
            logging.info("Reloaded exchange rates")

    def _get_exchange_rate(self, from_currency, to_currency):
        """Calculate exchange rate between two currencies."""
        self._maybe_reload_rates()

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Check if currencies exist
        if from_currency not in self.exchange_rates['rates']:
            return None, f"Currency {from_currency} not found"
        if to_currency not in self.exchange_rates['rates']:
            return None, f"Currency {to_currency} not found"

        # Calculate exchange rate
        base_currency = self.exchange_rates['base']
        
        # If the base currency is one of our currencies, direct conversion
        if base_currency == from_currency:
            rate = self.exchange_rates['rates'][to_currency]
        elif base_currency == to_currency:
            rate = 1 / self.exchange_rates['rates'][from_currency]
        else:
            # Cross-currency conversion via the base currency
            from_rate = self.exchange_rates['rates'][from_currency]
            to_rate = self.exchange_rates['rates'][to_currency]
            # First convert from source to base, then from base to target
            rate = to_rate / from_rate

        return rate, None

    def Convert(self, request, context):
        """Convert amount from one currency to another."""
        logging.info(f"Convert request: {request.from_currency} -> {request.to_currency}, amount: {request.amount}")
        
        rate, error = self._get_exchange_rate(request.from_currency, request.to_currency)
        
        if error:
            return currency_pb2.ConversionResponse(
                success=False,
                error_message=error,
                from_currency=request.from_currency.upper(),
                to_currency=request.to_currency.upper()
            )
        
        converted_amount = request.amount * rate
        
        return currency_pb2.ConversionResponse(
            converted_amount=round(converted_amount, 2),
            from_currency=request.from_currency.upper(),
            to_currency=request.to_currency.upper(),
            exchange_rate=rate,
            success=True
        )

    def GetExchangeRate(self, request, context):
        """Get exchange rate between two currencies."""
        logging.info(f"Exchange rate request: {request.from_currency} -> {request.to_currency}")
        
        rate, error = self._get_exchange_rate(request.from_currency, request.to_currency)
        
        if error:
            return currency_pb2.ExchangeRateResponse(
                success=False,
                error_message=error
            )
        
        return currency_pb2.ExchangeRateResponse(
            exchange_rate=rate,
            success=True
        )

    def GetAvailableCurrencies(self, request, context):
        """Get list of all available currencies."""
        logging.info("Request for available currencies")
        self._maybe_reload_rates()
        
        currencies = list(self.exchange_rates['rates'].keys())
        
        return currency_pb2.CurrenciesResponse(
            currencies=currencies,
            success=True
        )


def serve(port=50051, exchange_rates_file='exchange_rates.json'):
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_pb2_grpc.add_CurrencyConverterServicer_to_server(
        CurrencyConverterServicer(exchange_rates_file), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Server started, listening on port {port}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Server stopping...")
        server.stop(0)


if __name__ == '__main__':
    serve()