from elasticsearch import Elasticsearch
import wikipedia
import re


# Create for local node and create index
client = Elasticsearch()
index_name = "medical"

if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name)

# Schema declaration
disease_mapping = {
    'properties': {
        'name': {'type': 'text'},
        'title': {'type': 'text'},
        'full_text': {'type': 'text'},
    }
}

# Assign schema mapping
client.indices.put_mapping(
    index=index_name,
    doc_type='diseases',
    body=disease_mapping
)

diseased_links = wikipedia.page(title='List_of_diseases')

# Only get "List of diseases..." links
alpha_links = []
pattern = re.compile("List of diseases*")
for link in diseased_links.links:
    if pattern.match(link):
        try:
            alpha_links.append(link)
        except Exception as e:
            print(e)

# Parse and create indexes
doc_type = 'diseases'
for disease in alpha_links:
    try:
        current_page = wikipedia.page(disease)
        client.index(
            index=index_name,
            doc_type=doc_type,
            id=disease,
            body={
                'name': disease,
                'title': current_page.title,
                'full_text': current_page.content
            }
        )
    except Exception as e:
        print(e)


if __name__=='__main__':
    pass