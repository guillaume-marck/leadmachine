#!/usr/bin/env python3
"""
LeadMachine - Generateur de Prospects Locaux
Utilise l'API Recherche d'Entreprises du gouvernement francais (gratuite)

Usage:
    python lead_generator.py --secteur "boulangerie" --ville "Lyon" --nombre 50
    python lead_generator.py --secteur "plombier" --departement "69" --nombre 100
"""
import argparse, csv, json, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime

def search_api(query, departement="", ville="", page=1, per_page=25):
    params = {"q": query, "page": page, "per_page": per_page}
    if departement: params["departement"] = departement
    if ville: params["commune"] = ville
    url = f"https://recherche-entreprises.api.gouv.fr/search?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LeadMachine/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"[!] Erreur: {e}")
        return {"results": [], "total_results": 0}

def extract(results):
    leads = []
    for item in results:
        s = item.get("siege", {})
        addr = " ".join(filter(None, [s.get("numero_voie",""), s.get("type_voie",""), s.get("libelle_voie","")]))
        dirs = item.get("dirigeants", [])
        dn = f"{dirs[0].get('prenom','')} {dirs[0].get('nom','')}".strip() if dirs else ""
        leads.append({"entreprise": item.get("nom_complet","N/A"), "dirigeant": dn,
            "activite": s.get("libelle_activite_principale",""), "adresse": addr,
            "code_postal": s.get("code_postal",""), "ville": s.get("libelle_commune",""),
            "siren": item.get("siren",""), "siret": s.get("siret",""),
            "effectif": item.get("tranche_effectif_salarie",""), "date_creation": item.get("date_creation","")})
    return leads

def main():
    p = argparse.ArgumentParser(description="LeadMachine - Prospects Locaux")
    p.add_argument("--secteur", required=True)
    p.add_argument("--ville", default="")
    p.add_argument("--departement", default="")
    p.add_argument("--nombre", type=int, default=50)
    p.add_argument("--output", default="")
    a = p.parse_args()
    print(f"LeadMachine v1.0 | {a.secteur} | {a.ville or a.departement or 'France'} | {a.nombre} prospects")
    all_leads, page = [], 1
    while len(all_leads) < a.nombre:
        data = search_api(a.secteur, a.departement, a.ville, page)
        r = data.get("results", [])
        if not r: break
        all_leads.extend(extract(r))
        if page * 25 >= data.get("total_results", 0): break
        page += 1; time.sleep(0.5)
    all_leads = all_leads[:a.nombre]
    fn = a.output or f"leads_{a.secteur}_{a.ville or a.departement or 'france'}_{datetime.now().strftime('%Y-%m-%d')}.csv".replace(" ","_").lower()
    if all_leads:
        with open(fn, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(all_leads[0].keys()), delimiter=";")
            w.writeheader(); w.writerows(all_leads)
        print(f"[OK] {len(all_leads)} prospects -> {fn}")
    else: print("[!] Aucun resultat")

if __name__ == "__main__": main()
