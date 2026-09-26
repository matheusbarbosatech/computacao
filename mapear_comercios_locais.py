# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

lat, lon = -22.882226, -43.589861
radius = 3500

query = f"""
[out:json][timeout:35];
(
  node["amenity"~"dentist|clinic|doctors|pharmacy|veterinary|lawyer|school|restaurant|cafe"](around:{radius},{lat},{lon});
  node["office"~"lawyer|estate_agent|accountant|company|insurance"](around:{radius},{lat},{lon});
  node["shop"~"beauty|hairdresser|optician|car_repair|car|clothes|supermarket|bakery|pet"](around:{radius},{lat},{lon});
  way["amenity"~"dentist|clinic|doctors|pharmacy|school"](around:{radius},{lat},{lon});
  way["shop"~"supermarket|car_repair|beauty"](around:{radius},{lat},{lon});
);
out center 150;
"""

url = "https://overpass-api.de/api/interpreter"
data = urllib.parse.urlencode({"data": query}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"User-Agent": "MatheusLocalProspector/1.0"})

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        elements = res.get("elements", [])
        print(f"Total de nós/elementos retornados: {len(elements)}")
        businesses = []
        for el in elements:
            tags = el.get("tags", {})
            name = tags.get("name")
            if name:
                lat_val = el.get("lat") or (el.get("center", {}).get("lat"))
                lon_val = el.get("lon") or (el.get("center", {}).get("lon"))
                b_type = tags.get("amenity") or tags.get("office") or tags.get("shop")
                phone = tags.get("phone") or tags.get("contact:phone") or tags.get("contact:whatsapp") or tags.get("contact:mobile") or ""
                website = tags.get("website") or tags.get("contact:website") or ""
                street = tags.get("addr:street", "")
                num = tags.get("addr:housenumber", "")
                
                businesses.append({
                    "nome": name,
                    "categoria": b_type,
                    "endereco": f"{street} {num}".strip(),
                    "telefone": phone,
                    "website": website,
                    "lat": lat_val,
                    "lon": lon_val
                })
                
        print(f"Comércios com nome mapeados: {len(businesses)}")
        with open("comercios_campo_grande.json", "w", encoding="utf-8") as f:
            json.dump(businesses, f, ensure_ascii=False, indent=2)
            
        print("Primeiros 20 resultados:")
        for b in businesses[:20]:
            print(f"- [{b['categoria']}] {b['nome']} | {b['endereco']} | Tel: {b['telefone']} | Site: {b['website']}")

except Exception as e:
    print("Erro ao consultar Overpass:", e)
