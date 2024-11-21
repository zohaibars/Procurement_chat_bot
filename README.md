# Procurement RAG Chatbot

A FastAPI-based intelligent procurement analysis system that uses Retrieval-Augmented Generation (RAG) to provide insights from procurement data. The system combines MongoDB for data storage, ChromaDB for vector storage, and Groq's LLM for intelligent query processing.

## 🌟 Features

- **Intelligent Query Processing**: Uses RAG architecture to provide context-aware responses
- **Procurement Data Analysis**: Analyzes spending patterns and procurement trends
- **Real-time Stats**: Provides summary statistics of procurement data
- **Modular Architecture**: Well-organized codebase for easy maintenance and scaling
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## 🔧 Tech Stack

- FastAPI
- MongoDB
- ChromaDB
- Groq LLM
- LangChain
- HuggingFace Embeddings
- Python 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- MongoDB installed and running
- Groq API key
- Git


## 📊 Data Management

### Initial Data Loading

The system expects a CSV file with procurement data. The path to this file should be specified in the `.env` file:

```env
CSV_DATA_PATH=data_tests/PURCHASE ORDER DATA EXTRACT 2012-2015_0.csv

unzip: data_tests/PURCHASE ORDER DATA EXTRACT 2012-2015_0.rar
```


The data will be automatically loaded into MongoDB when the application starts if the collection is empty.

### Data Loading Endpoints

- `POST /data/load`
  - Manually trigger data loading process
  - Runs in the background
  - Response: `{"message": "Data loading process started"}`

- `GET /data/status`
  - Check the status of data in MongoDB
  - Response: 
    ```json
    {
        "documents_count": 1234,
        "status": "Data loaded successfully"
    }
    ```

### Data Directory Structure

```
procurement-rag-chatbot/
├── data_tests/
│   └── PURCHASE ORDER DATA EXTRACT 2012-2015_0.csv
```

### CSV Data Format

The CSV file should contain the following columns:
- Purchase Order Number
- Creation Date
- Department Name
- Supplier Name
- Item Name
- Item Description
- Quantity
- Unit Price
- Total Price
- Fiscal Year


## 🚀 Getting Started


1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/procurement-rag-chatbot.git
   cd procurement-rag-chatbot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory and add the following variables:
   ```env
   # MongoDB Configuration
   MONGODB_URL=mongodb://localhost:27017/
   MONGODB_DB=procurement_db
   MONGODB_COLLECTION=procurement_data

   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=5005
   DEBUG=True

   # Model Configuration
   GROQ_API_KEY=your_groq_api_key
   EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
   LLM_MODEL=llama-3.1-70b-versatile

   # Vector DB Configuration
   CHROMA_DB_PATH=./chroma_db
   ```

5. **Run the application**


   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:5005`

## 📚 API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:5005/docs`
- ReDoc: `http://localhost:5005/redoc`

### Key Endpoints

- `POST /chat`
  - Submit questions about procurement data
  - Request body: `{"text": "your question here"}`

- `GET /stats/summary`
  - Get summary statistics of procurement data

## 🗄️ Project Structure

```
├── .env
├── .gitignore
├── requirements.txt
├── main.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── app/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   ├── routes.py
    │   └── models.py
    ├── core/
    │   ├── __init__.py
    │   ├── database.py
    ├── services/
    │   ├── __init__.py
    │   ├── rag_service.py
    │   └── analysis_service.py
    └── utils/
        ├── __init__.py
        └── data_loader.py

```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔒 Security

- Never commit your `.env` file
- Keep your Groq API key secure
- Regularly update dependencies
- Follow security best practices when deploying
