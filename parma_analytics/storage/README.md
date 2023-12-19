# Firebase storage schema

The diagram provided illustrates the Firebase storage structure specific to our project.
Within this schema, it's important to note that for the analytics repository, only the
'reports' branch is pertinent. This branch is utilized for both storing generated
reports and retrieving stored ones.

```mermaid
    graph TD
    B[Storage Bucket]
    B -->|Contains| D[user]
    B -->|Contains| E[company]
    B -->|Contains| N[reports]

    D -->|For each user| F{profile_photos}
    F --> G["user_pic_ref1"]
    F --> H["user_pic_ref2"]
    F --> I["user_pic_ref3"]

    E -->|For each company| J{companies}
    J -->|company 1| K["attachment_ref1"]
    J -->|company 2| L["attachment_ref2"]
    J -->|company N| M["attachment_ref3"]

    N -->|For each company| O{companies}
    N -->|For each user| P{user}
    P -->|user 1| S[report_2020-11-11]
    P -->|user 2| Q[report_2023-12-23]
    P -->|user N| R[report_2021-02-21]
    O -->|company 1| T[report_2020-11-11]
    O -->|company 2| U[report_2023-12-23]
    O -->|company N| V[report_2021-02-21]
```
