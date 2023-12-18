# Firebase storage schema

graph TD
B[Storage Bucket]
B -->|Contains| D[user]
B -->|Contains| E[company]
B -->|Contains| N[reports]

D -->|For each user| F{Profile Photos}
F --> G[user 1 pic]
F --> H[user 2 pic]
F --> I[user N pic]

E -->|For each company| J{companies}
J -->|company 1| K[Attachments]
J -->|company 2| L[Attachments]
J -->|company N| M[Attachments]

N -->|For each company| O{companies}
N -->|For each user| P{user}
P -->|user 1| S[report_11.11.20]
P -->|user 2| Q[report_11.12.23]
P -->|user N| R[report_11.02.21]
O -->|company 1| T[report_11.11.20]
O -->|company 2| U[report_11.12.23]
O -->|company N| V[report_11.02.21]
