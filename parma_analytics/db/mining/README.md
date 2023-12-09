# Firestore database

## Database schema

### Collection hierarchy

#### visualization as collection

```mermaid
graph LR;
    subgraph parma/mining/
        subgraph datasource/DATASOURCE_NAME/
            subgraph raw_data/
                ut1(RAW_DATA1)
                ut2(RAW_DATA2)
            end
            subgraph normalization_schema
                ut3(SCHEMA_1)
                ut4(SCHEMA_2)
            end
        end
        subgraph trigger/
            ut5(TRIGGER1)
            ut6(TRIGGER2)
        end
    end
    subgraph parma/frontend/
        subgraph todo
        end
    end
    subgraph parma/analytics/
        subgraph todo.
        end
    end
```

#### visualization as tree

```mermaid
stateDiagram-v2
    parma --> mining
        mining --> datasource
        mining --> trigger
        datasource --> DATASOURCE_NAME1
        DATASOURCE_NAME1 --> raw_data
        DATASOURCE_NAME1 --> normalization_schema

            raw_data --> RAW_DATA1
            raw_data --> RAW_DATA2

            normalization_schema --> SCHEMA1
            normalization_schema --> SCHEMA2

        trigger --> TRIGGER1
        trigger --> TRIGGER2

    parma --> frontend
    parma --> analytics
```

### Document models

```mermaid
erDiagram
    "parma/mining/datasource/NAME/raw_data/DOCUMENT_ID" {
        uuid DOCUMENT_ID "PK"
        ref mining_trigger "FK"
        string status "success | failure"
        map data "actually mined json"
    }
    "parma/mining/datasource/NAME/normalization_schema/DOCUMENT_ID" {
        uuid DOCUMENT_ID "PK"
        map schema ""
    }
    "parma/mining/trigger/DOCUMENT_ID" {
        uuid DOCUMENT_ID "PK"
        reference datasource "FK"
        string started_at ""
        string finished_at ""
        int scheduled_task_id "FK (to SQL)"
        string status ""
        string note "optional"
    }
```
