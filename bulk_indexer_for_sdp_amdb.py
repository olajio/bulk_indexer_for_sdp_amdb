from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import copy
import os
import json # Import the json module to read JSON files

# --- Configuration ---
ES_HOST = "http://localhost:9200" # Replace with your Elasticsearch host and port
ES_INDEX = "sdp_amdb"
HOSTNAMES_FILE = "hostnames.txt"   # Name of the file containing hostnames
BASE_FIELDS_FILE = "base_fields.json" # Name of the file containing base document fields

# --- Helper Function to Read Any JSON File ---
def read_json_file(filename):
    """Reads and parses a JSON file into a Python dictionary."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print(f"Read configuration from '{file_path}'")
        return data
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        print(f"Please ensure '{filename}' is in the same directory as the script.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        print("Please check the JSON syntax (e.g., missing commas, unquoted keys/strings).")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
        exit(1)

# --- Function to read hostnames from file ---
def read_hostnames_from_file(filename):
    hostnames = []
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    try:
        with open(file_path, 'r') as f:
            for line in f:
                hostname = line.strip()
                if hostname:
                    hostnames.append(hostname)
        print(f"Read {len(hostnames)} hostnames from '{file_path}'")
    except FileNotFoundError:
        print(f"Error: Hostnames file '{file_path}' not found.")
        print("Please ensure 'hostnames.txt' is in the same directory as the script.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while reading the hostnames file: {e}")
        exit(1)
    return hostnames

# --- Script Logic (Remains largely the same) ---
def create_documents_from_hostnames(es_client, index_name, hostnames, base_fields):
    """
    Generates and indexes documents for a list of hostnames,
    using a base set of fields.
    """
    actions = []
    if not hostnames:
        print("No hostnames found to process. Exiting.")
        return

    for hostname in hostnames:
        # Create a deep copy of the base fields to avoid modifying the original
        doc_source = copy.deepcopy(base_fields)
        doc_source["hostname"] = hostname # Add the unique hostname to the document

        action = {
            "_index": index_name,
            "_id": hostname, # Use the hostname as the document ID
            "_source": doc_source
        }
        actions.append(action)

    print(f"Preparing to index {len(actions)} documents into index '{index_name}'...")

    try:
        success, failed = bulk(es_client, actions, stats_only=True)

        print(f"Bulk indexing complete:")
        print(f"  Successfully indexed: {success} documents")
        print(f"  Failed to index: {failed} documents")

        if failed > 0:
            print("\nSome documents failed to index. Check Elasticsearch logs for details.")

    except Exception as e:
        print(f"An error occurred during bulk indexing: {e}")

# --- Main execution ---
if __name__ == "__main__":
    try:
        # Initialize the Elasticsearch client
        es = Elasticsearch(ES_HOST)

        # Verify connection
        if not es.ping():
            raise ValueError("Connection to Elasticsearch failed!")
        print(f"Successfully connected to Elasticsearch at {ES_HOST}")

        # Read hostnames from the file
        hostnames_to_create = read_hostnames_from_file(HOSTNAMES_FILE)

        # Read base document fields from the JSON file
        base_document_fields = read_json_file(BASE_FIELDS_FILE)

        # Execute the function to create documents
        create_documents_from_hostnames(es, ES_INDEX, hostnames_to_create, base_document_fields)

    except Exception as e:
        print(f"Script error: {e}")
