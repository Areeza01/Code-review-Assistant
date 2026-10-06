## Environment Variables

This project uses environment variables to securely store Azure credentials and configuration.

### 1. Create a `.env` file

After cloning the repository, create a new file named:

```text
.env
```

in the root directory of the project.

### 2. Add your Azure credentials

Add the following variables to your `.env` file:

```env
PROJECT_ENDPOINT=YOUR_PROJECT_ENDPOINT
AZURE_STORAGE_CONNECTION_STRING=AZURE_STORAGE_CONNECTION_STRING
DATABASE_URL=YOUR_DATABASE_URL
```

Replace the placeholder values with your own Azure Storage Account credentials.

### 3. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the project

After creating and configuring your `.env` file, run the project using:

```bash
python app.py
```

> **Note:** The `.env` file is intentionally not included in this repository because it contains sensitive credentials. Each user must create their own `.env` file using their own Azure credentials.

### `.env.example`

For reference, the required environment variables are:

```env
PROJECT_ENDPOINT=YOUR_PROJECT_ENDPOINT
AZURE_STORAGE_CONNECTION_STRING=AZURE_STORAGE_CONNECTION_STRING
DATABASE_URL=YOUR_DATABASE_URL
```

Never commit your actual `.env` file or expose your Azure credentials publicly.
