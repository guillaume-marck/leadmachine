# LeadMachine

Service de generation de prospects locaux qualifies pour entreprises et independants.

## Fonctionnement

Chaque mois, vos clients recoivent une liste de 50 a 100 prospects qualifies dans leur zone geographique et leur secteur d'activite.

## Outil de generation

```bash
python tools/lead_generator.py --secteur "boulangerie" --departement "75" --nombre 50
```

Options:
- `--secteur` : Secteur d'activite (obligatoire)
- `--ville` : Filtrer par ville
- `--departement` : Filtrer par departement
- `--nombre` : Nombre de prospects (defaut: 50)
- `--output` : Nom du fichier de sortie

## Source des donnees

API Recherche d'Entreprises du gouvernement francais (gratuite, legale, donnees publiques).
