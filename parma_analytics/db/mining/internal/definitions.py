"""In code defined schema for the mining database."""

from parma_analytics.db.mining.internal.models import (
    Collection,
    Doc,
    DocField,
    DocTemplate,
)

# ------------------------------------------------------------------------------------ #
#                             schema definition: bottom up                             #
# ------------------------------------------------------------------------------------ #

# mining

doc_trigger = DocTemplate(
    fields={
        "datasource": DocField(name="datasource", type="reference"),
        "started_at": DocField(name="started_at", type="timestamp"),
        "finished_at": DocField(name="finished_at", type="timestamp"),
        "scheduled_task_id": DocField(name="scheduled_task_id", type="boolean"),
        "status": DocField(name="status", type="string"),
        "note": DocField(name="note", type="string", required=False),
    }
)
col_trigger = Collection(name="trigger", docs=doc_trigger)

doc_raw_data = DocTemplate(
    fields={
        "mining_trigger": DocField(name="mining_trigger", type="reference"),
        "status": DocField(name="status", type="string"),
        "data": DocField(name="data", type="map"),
    }
)
col_raw_data = Collection(name="raw_data", docs=doc_raw_data)

doc_normalized_data = DocTemplate(
    fields={
        "raw_data": DocField(name="raw_data", type="reference"),
        "normalized_at": DocField(name="normalized_at", type="timestamp"),
        "status": DocField(name="status", type="string"),
        "data": DocField(name="data", type="map"),
    }
)
col_normalized_data = Collection(name="normalized_data", docs=doc_normalized_data)

doc_datasource = DocTemplate(
    collections={"raw_data": col_raw_data, "normalized_data": col_normalized_data},
)
col_datasource = Collection(name="datasource", docs=doc_datasource)

doc_mining = Doc(
    name="mining",
    collections={
        "trigger": col_trigger,
        "datasource": col_datasource,
    },
)

# frontend

doc_frontend = Doc(name="frontend")

# analytics

doc_analytics = Doc(name="analytics")

# ------------------------------- Top level collection ------------------------------- #

parma_collection = Collection(
    name="parma",
    docs={"mining": doc_mining, "frontend": doc_frontend, "analytics": doc_analytics},
)
