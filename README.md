# Elasticsearch Bulk Host Indexer for sdp_amdb

This Python script provides a robust and flexible way to bulk index host-related documents into an Elasticsearch index. It's designed to read a list of hostnames from a text file and apply a common set of document fields (read from a JSON file) to each, using the hostname as the document's unique ID.

## Features

* **Configurable Elasticsearch Connection:** Easily set your Elasticsearch host.
* **External Host List:** Read hostnames from a simple text file (`hostnames.txt`), making it easy to manage your host inventory.
* **External Base Document Fields:** Define common document fields in a JSON file (`base_fields.json`), allowing for easy updates to your schema without touching the code.
* **Efficient Bulk Indexing:** Utilizes Elasticsearch's `_bulk` API via the `elasticsearch-py` client's helper for optimal performance.
* **Error Handling:** Basic error handling for file operations and Elasticsearch connection.

## Prerequisites

Before running the script, make sure you have:

* **Python 3.x:** Installed on your system.
* **Elasticsearch Cluster:** A running Elasticsearch instance that the script can connect to.
* **`elasticsearch` Python Client:** Install it using pip:
    ```bash
    pip install elasticsearch
    ```

## Setup and Configuration

1.  **Save the Script:**
    Save the provided Python code into a file named `index_hosts.py` (or any other `.py` extension).

2.  **Create `hostnames.txt`:**
    In the **same directory** as your `index_hosts.py` script, create a text file named `hostnames.txt`.
    List each hostname on a new line.

    **`hostnames.txt` example:**
    ```
    ES01-ESXCB300-DS04
    ES02-WEBA100-SQL01
    PROD-WEB-001
    TEST-DB-002
    ```

3.  **Create `base_fields.json`:**
    In the **same directory** as your `index_hosts.py` script, create a JSON file named `base_fields.json`.
    Define the common fields that will be applied to all documents (excluding the `hostname` field, which is added dynamically).

    **`base_fields.json` example:**
    ```json
    {
      "group": ["11115"],
      "app_code": "",
      "alert_status": "enabled",
      "type": "datastore",
      "environment": "development",
      "region": "us-east-1"
    }
    ```
    **Important:** Ensure your JSON is valid. Keys and string values must be enclosed in double quotes.

4.  **Configure Script Variables:**
    Open `index_hosts.py` and adjust the following variables at the top of the script as needed:

    * `ES_HOST`: Your Elasticsearch cluster's URL (e.g., `"http://localhost:9200"` or `"https://your-es-cluster:9200"`).
    * `ES_INDEX`: The name of the Elasticsearch index where documents will be stored (e.g., `"sdp_amdb"`).
    * `HOSTNAMES_FILE`: The filename for your host list (default: `"hostnames.txt"`).
    * `BASE_FIELDS_FILE`: The filename for your base document fields (default: `"base_fields.json"`).

## Usage

Once you've completed the setup and configuration steps, run the script from your terminal:

```bash
python index_hosts.py
```

The script will:

1.  Connect to your Elasticsearch cluster.
2.  Read the hostnames from `hostnames.txt`.
3.  Read the base document fields from `base_fields.json`.
4.  Construct a unique document for each hostname by combining the hostname with the base fields.
5.  Perform a bulk index operation, using each hostname as the document's `_id` in the `sdp_amdb` index.
6.  Report on the success and failure counts of the indexed documents.

---

### Need to expand the functionality or tailor it further?

Feel free to open an issue or suggest an improvement if you have specific features in mind!
