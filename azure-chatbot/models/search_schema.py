from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchSuggester,
    SemanticConfiguration,
    SemanticPrioritizedFields
)

def get_index_schema(index_name: str) -> SearchIndex:
    """Return index schema including fileName, content, description, blobPath."""
    fields = [
        SimpleField(name="id", type="Edm.String", key=True, filterable=True),
        SearchableField(name="blobName", type="Edm.String", searchable=True, retrievable=True, filterable=True),
        SearchableField(name="content", type="Edm.String", searchable=True, retrievable=True),
        SearchableField(name="description", type="Edm.String", searchable=True, retrievable=True, filterable=True),
        SimpleField(name="blobPath", type="Edm.String", retrievable=True)
    ]

    suggester = SearchSuggester(
        name="sg",
        source_fields=["blobName", "description"]
    )

    # Define semantic configuration
    semantic_config = SemanticConfiguration(
        name="default",
        prioritized_fields=SemanticPrioritizedFields(
            title_field="blobName",
            content_fields=["content", "description"]
        )
    )

    return SearchIndex(
        name=index_name,
        fields=fields,
        suggesters=[suggester],
        semantic_configurations=[semantic_config]
    )
