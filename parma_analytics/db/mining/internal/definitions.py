"""In code defined schema for the mining database."""

from parma_analytics.db.mining.internal.models import (
    Collection,
    Doc,
    DocField,
    DocTemplate,
)

# --------------------------------- schema definition -------------------------------- #

# mining

doc_mining = Doc(
    name="mining",
    collections={
        "trigger": Collection(
            name="trigger",
            docs=DocTemplate(
                fields={
                    "datasource": DocField(name="datasource", type="reference"),
                    "started_at": DocField(name="started_at", type="timestamp"),
                    "finished_at": DocField(name="finished_at", type="timestamp"),
                    "scheduled_task_id": DocField(
                        name="scheduled_task_id", type="number"
                    ),
                    "status": DocField(name="status", type="string"),
                    "note": DocField(name="note", type="string", required=False),
                }
            ),
        ),
        "datasource": Collection(
            name="datasource",
            docs=DocTemplate(
                collections={
                    "raw_data": Collection(
                        name="raw_data",
                        docs=DocTemplate(
                            fields={
                                "mining_trigger": DocField(
                                    name="mining_trigger", type="reference"
                                ),
                                "status": DocField(name="status", type="string"),
                                "company_id": DocField(
                                    name="company_id", type="string"
                                ),
                                "data": DocField(name="data", type="map"),
                            }
                        ),
                    ),
                    "normalization_schema": Collection(
                        name="normalization_schema",
                        docs=DocTemplate(
                            fields={
                                "schema": DocField(name="schema", type="map"),
                            }
                        ),
                    ),
                },
            ),
        ),
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
