# gRPC Currency Conversion Microservice

A real-time currency conversion microservice built using gRPC. This service provides currency conversion functionality based on exchange rates.

## Features

- Convert amounts between different currencies
- Get exchange rates between currency pairs
- List all available currencies
- Automatic periodic reload of exchange rates

## Project Structure

```
currency-conversion-service/
├── currency.proto          # gRPC service definition
├── grpc_server.py          # Server implementation
├── grpc_client.py          # Client application
├── exchange_rates.json     # Sample exchange rate data
├── README.md               # This file
```

## Prerequisites

- Python 3.7 or higher
- gRPC and protobuf packages

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd currency-conversion-service
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install grpcio grpcio-tools
   ```

4. Generate gRPC code from protocol buffer definition:
   ```
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. currency.proto
   ```

## Running the Service

1. Start the gRPC server:
   ```
   python grpc_server.py
   ```

2. In a separate terminal, run the client:
   ```
   python grpc_client.py
   ```

## Using the Client

The client provides an interactive command-line interface with the following commands:

1. **Convert currency**:
   ```
   convert <from_currency> <to_currency> <amount>
   ```
   Example: `convert USD EUR 100`

2. **Get exchange rate**:
   ```
   rate <from_currency> <to_currency>
   ```
   Example: `rate USD JPY`

3. **List available currencies**:
   ```
   currencies
   ```

4. **Exit the client**:
   ```
   exit
   ```

## Customizing Exchange Rates

The service uses exchange rates defined in `exchange_rates.json`. You can:

1. Update this file manually with new rates
2. Replace it with a file from an external source
3. Modify the server to fetch rates from an external API

The format of the exchange rates file should be:
```json
{
  "base": "USD",
  "last_updated": "2025-03-22T12:00:00Z",
  "rates": {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.78,
    ...
  }
}
```

## Advanced Usage

### Running the server with custom port:

```
python grpc_server.py --port 50052
```

### Connecting the client to a remote server:

```
python grpc_client.py --host remote-server.example.com --port 50051
```

### Using the client programmatically:

```python
from grpc_client import CurrencyClient

# Create a client
client = CurrencyClient(host='localhost', port=50051)

# Convert currency
result = client.convert('USD', 'EUR', 100)
print(f"100 USD = {result.converted_amount} EUR")

# Get exchange rate
rate = client.get_exchange_rate('USD', 'GBP')
print(f"1 USD = {rate} GBP")

# List available currencies
currencies = client.get_available_currencies()
print(f"Available currencies: {', '.join(currencies)}")

# Close the client
client.close()
```

## Next Steps for Enhancement

- Add authentication and TLS
- Implement caching for better performance
- Add historical exchange rate support
- Create a REST API gateway for non-gRPC clients

## Author

[Zaid]