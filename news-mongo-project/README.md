# News Mongo Project

This project is designed to manage and store news articles in a MongoDB database. It provides a structured way to insert and retrieve articles while ensuring data integrity through schema validation and unique indexing.

## Project Structure

```
news-mongo-project
├── src
│   ├── db
│   │   ├── connection.py      # Handles MongoDB connection
│   │   └── schema.py          # Defines the article schema
│   ├── models
│   │   └── article.py         # Contains functions for article operations
│   ├── main.py                # Entry point of the application
├── .env                        # Environment variables for configuration
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd news-mongo-project
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   Ensure you have `pymongo` and `python-dotenv` installed by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your MongoDB connection string:
   ```
   MONGO_URI="mongodb://localhost:27017/"
   ```

## Usage

To run the application, execute the following command:
```bash
python src/main.py
```

This will connect to the MongoDB database, define a sample article, and insert it into the `articles` collection. A confirmation message will be printed upon successful insertion.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.