# Elasticsearch Bulk Host Indexer

This Python script offers a robust and flexible way to create sdp_amdb records in the sdp_amdb index. It is harcoded to index into our CCS Elasticsearch cluster. It's designed to read a list of hostnames from a text file, authenticate to Elasticsearch with an API key and apply a common set of fields (read from a JSON file) to each record. The script uses the hostname as the document id.

## Features

* **Configurable Elasticsearch Connection:** Easily set your Elasticsearch host.
* **External Host List:** Reads hostnames from a simple text file (`hostnames.txt`), making it easy to manage your host inventory.
* **External Base Document Fields:** Defines common document fields in a JSON file (`base_fields.json`), allowing for easy updates to the schema without touching the code.
* **API Key Authentication:** Securely connects to Elasticsearch using an API key (read from `es_auth.json`).
* **Efficient Bulk Indexing:** Utilizes Elasticsearch's `_bulk` API.
* **Dependency Management:** Includes a `requirements.txt` file for easy setup of the Python environment.
* **Error Handling:** Provides basic error handling for file operations and Elasticsearch connection.

---

## Prerequisites

Before running the script, make sure you have:

* **Python 3.x:** Installed on your system.
* **Elasticsearch Cluster:** A running Elasticsearch instance that the script can connect to.
* **Elasticsearch API Key:** An API key with sufficient privileges (e.g., `write`, `create`, `create_doc`, `index` on the target index) generated from your Elasticsearch cluster.
* **Python Dependencies:** Install the necessary libraries using `pip` and the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

---

## Setup and Configuration

1.  **Save the Script:**
    Save the provided Python code into a file named `index_hosts.py` (or any other `.py` extension).

2.  **Create `hostnames.txt`:**
    In the **same directory** as your `index_hosts.py` script, create a text file named `hostnames.txt`. List each hostname on a new line.

    **`hostnames.txt` example:**
    ```
    CS01-10PRODPY21
    PROD-WEB-001
    TEST-DB-002
    ```

3.  **Create `base_fields.json`:**
    In the **same directory** as your `index_hosts.py` script, create a JSON file named `base_fields.json`. Define the common fields that will be applied to all documents (excluding the `hostname` field, which is added dynamically).

    **`base_fields.json` example:**
    ```json
    {
      "group": ["11115"],
      "app_code": "",
      "alert_status": "enabled",
      "type": "datastore"
    }
    ```
    **Important:** Ensure your JSON is valid. Keys and string values must be enclosed in double quotes.

4.  **Create `es_auth.json`:**
    In the **same directory** as your `index_hosts.py` script, create a JSON file named `es_auth.json`. This file will securely store your Elasticsearch API Key ID and Secret.

    **`es_auth.json` example:**
    ```json
    {
      "api_key_id": "YOUR_ELASTICSEARCH_API_KEY_ID_HERE",
      "api_key_secret": "YOUR_ELASTICSEARCH_API_KEY_SECRET_HERE"
    }
    ```

5.  **Configure Script Variables:**
    Open `index_hosts.py` and adjust the following variables at the top of the script as needed:

    * `ES_HOST`: Your Elasticsearch cluster's URL (e.g., `"http://localhost:9200"` or `"https://your-es-cluster:9200"`).
    * `ES_INDEX`: The name of the Elasticsearch index where documents will be stored (e.g., `"sdp_amdb"`).
    * `HOSTNAMES_FILE`: The filename for your host list (default: `"hostnames.txt"`).
    * `BASE_FIELDS_FILE`: The filename for your base document fields (default: `"base_fields.json"`).
    * `ES_AUTH_FILE`: The filename for your API key credentials (default: `"es_auth.json"`).

---

## Usage

Once you've completed the setup and configuration steps, run the script from your terminal:

```bash
python index_hosts.py
```

The script will:

1.  Connect to your Elasticsearch cluster using the provided API key.
2.  Read the hostnames from `hostnames.txt`.
3.  Read the base document fields from `base_fields.json`.
4.  Construct a unique document for each hostname by combining the hostname with the base fields.
5.  Perform a bulk index operation, using each hostname as the document's `_id` in the specified sdp_amdb index.
6.  Report on the success and failure counts of the indexed documents.

---
