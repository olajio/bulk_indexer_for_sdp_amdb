# Elasticsearch Bulk Hosts Indexer to sdp_amdb

This Python script offers a robust and flexible way to create sdp_amdb records in the sdp_amdb index. It is harcoded to index into an CCS Elasticsearch cluster, but the Elasticsearch endpoint can be easily chnaged to apply this script to any cluster. It's designed to read a list of hostnames from a text file, authenticate to Elasticsearch with an API key and apply a common set of fields (read from a JSON file) to each record. The script uses the hostname as the document id.

## Features

* **Configurable Elasticsearch Connection:** Easily set the Elasticsearch host.
* **External Host List:** Reads hostnames from a simple text file (`hostnames.txt`), making it easy to manage the host inventory.
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
* **Elasticsearch API Key:** An API key with sufficient privileges (e.g., `write`, `create`, `create_doc`, `index` on the target index) generated from the Elasticsearch cluster.
* **Python Dependencies:** Install the necessary libraries using `pip` and the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

---

## Setup and Configuration

1.  **Save the Script:**
    Save the provided Python code into a file named `index_hosts.py`.

2.  **Create `hostnames.txt`:**
    In the **same directory** as the `index_hosts.py` script, create a text file named `hostnames.txt`. List each hostname on a new line.

    **`hostnames.txt` example:**
    ```
    HOSTNAME1
    HOSTNAME2
    HOSTNAME3
    ```

3.  **Create `base_fields.json`:**
    In the **same directory** as the `index_hosts.py` script, create a JSON file named `base_fields.json`. Define the common fields that will be applied to all documents (excluding the `hostname` field, which is added dynamically).

    **`base_fields.json` example:**
    ```json
    {
      "group": ["11115"],
      "app_code": "",
      "alert_status": "enabled",
      "type": "datastore"
    }
    ```

4.  **Create `es_auth.json`:**
    In the **same directory** as the `index_hosts.py` script, create a JSON file named `es_auth.json`. This file will securely store the Elasticsearch API Key ID and Secret.

    **`es_auth.json` example:**
    ```json
    {
      "api_key_id": "ELASTICSEARCH_API_KEY_ID_HERE",
      "api_key_secret": "ELASTICSEARCH_API_KEY_SECRET_HERE"
    }
    ```

5.  **Configure Script Variables:**
    Open `index_hosts.py` and adjust the following variables at the top of the script as needed:

    * `ES_HOST`: Elasticsearch endpoints's URL (e.g., `"http://localhost:9200"` or `"https://es-cluster:9200"`).
    * `ES_INDEX`: The name of the Elasticsearch index where documents will be stored (in this case, it is the `"sdp_amdb"` index).
    * `HOSTNAMES_FILE`: The filename for the host list (default: `"hostnames.txt"`).
    * `BASE_FIELDS_FILE`: The filename for the base document fields (in this case, the file is named: `"base_fields.json"`).
    * `ES_AUTH_FILE`: The filename for the API key credentials (in this case, the file is named: `"es_auth.json"`).

---

## Usage

Once you've completed the setup and configuration steps, run the script from the terminal or any other Python IDE:

```bash
python index_hosts.py
```

## Sample Output

If the script runs succesfully, the output would lookmlike the following image:

<img width="1063" alt="image" src="https://github.com/user-attachments/assets/672dfced-bf48-492a-b404-889538a4f5ab" />


In summary, the script will:

1.  Connect to the Elasticsearch cluster using the provided API key.
2.  Read the hostnames from `hostnames.txt`.
3.  Read the base document fields from `base_fields.json`.
4.  Construct a unique document for each hostname by combining the hostname with the base fields.
5.  Perform a bulk index operation, using each hostname as the document's `_id` in the specified sdp_amdb index.
6.  Report on the success and failure counts of the indexed documents.

---
