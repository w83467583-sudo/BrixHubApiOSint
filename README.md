BrixHub CLI Dashboard
BrixHub CLI Dashboard checks data from the BrixHub API and displays information via a terminal user interface.

Retrieves information using a dual-column layout.

Does not require heavy resources.

Runs on Python 3.

Installation
With PyPI
Bash
pip install windows-curses requests
With GitHub
Bash
git clone https://github.com/votre-profil/brixhub-dashboard.git
cd brixhub-dashboard
python test.py
Quick Start
The dashboard can be run directly from the CLI to search and export profiles.

CLI Example
Bash
python test.py
Python Example
Python
import curses
import requests

payload = {"prenom": "John", "nom_famille": "Doe"}
headers = {"X-API-Key": "YOUR_KEY"}
r = requests.post("https://brixhub.net/api/v1/search", json=payload, headers=headers)
print(r.json())
Module Output
For each profile, data is returned in a standard dictionary format:

JSON
{
  "prenom": "John",
  "nom_famille": "Doe",
  "email": "john.doe@email.com",
  "fivem_id": "fivem:123456",
  "_confidence": 95
}
