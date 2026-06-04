# Illustrasjon API Statistikkbanken

Dette prosjektet demonstrerer hvordan en ny statistikk-side kan bygges foran et eksisterende API.

Frontend viser:
- en ny brukerrettet side i venstre panel
- hva som skjer under panseret i hoyre panel

Backend fungerer som en liten proxy mot UDIR API-et slik at frontend slipper CORS-problemet ved direkte kall fra nettleseren.

## Filer

- `app.py`: FastAPI-backend som serverer frontend og videresender API-kall
- `index.html`: demo-frontend med 2/3 + 1/3 layout
- `requirements.txt`: Python-avhengigheter
- `.env.example`: valgfri eksempelkonfigurasjon
- `.gitignore`: filer som ikke skal pushes

## Hvordan det virker

1. Frontend sender `POST /api/statistikk` til egen backend.
2. Backend sender requesten videre til UDIR API-et med `text/plain` body og `radSti` som query-parameter.
3. Backend returnerer responsen til frontend.
4. Frontend viser både dataene og request/response-detaljene.

## Lokal kjoring

Prosjektet trenger Python med disse pakkene:

```bash
pip install -r requirements.txt
```

Start appen med:

```bash
uvicorn app:app --reload
```

Aapne deretter:

```text
http://127.0.0.1:8000
```

## Konfigurasjon

Appen kan kjore uten `.env` fordi den har standardverdier i `app.py`.
Hvis du vil overstyre disse, kan du kopiere `.env.example` til `.env` og justere verdiene.

## GitHub

Før push til GitHub anbefales dette oppsettet:

```bash
git init
git add .
git commit -m "Initial demo app"
```

Deretter kan du koble repoet til din egen GitHub remote og pushe dit.

## Azure

Dette oppsettet passer som et enkelt utgangspunkt for deploy til Azure App Service.
Senere kan du legge til:
- produksjonsorigins i CORS-oppsettet
- mer robust logging
- domenespesifikk transformasjon av statistikkresponsen
