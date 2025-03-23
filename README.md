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


## Next Steps for Enhancement

- Add authentication and TLS
- Implement caching for better performance
- Add historical exchange rate support
- Create a REST API gateway for non-gRPC clients
