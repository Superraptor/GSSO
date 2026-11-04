"""
Entity fetcher for lgbtDB with pagination, caching, and rate-limiting resilience.
"""

import os
import json
import time
import urllib.request
import urllib.parse
from typing import Dict, List, Set, Any, Optional

from .config import (
    API_URL,
    CACHE_DIR,
    USER_AGENT,
    PROP_SUBCLASS_OF,
    PROP_GSSO_V2_ID
)


class LGBTDBFetcher:
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir or CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        self.entities_cache_file = os.path.join(self.cache_dir, "entities.json")

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Performs an HTTP GET request to the MediaWiki API."""
        params["format"] = "json"
        query_str = urllib.parse.urlencode(params)
        url = f"{API_URL}?{query_str}"
        headers = {"User-Agent": USER_AGENT}

        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                wait_time = 2 ** attempt
                print(f"[Warning] API request failed ({e}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
        raise RuntimeError(f"Failed to query lgbtDB API after 4 attempts: {url}")

    def fetch_property_backlinks(self, property_id: str, max_items: Optional[int] = None) -> List[str]:
        """
        Fetches all Q-items that make reference to a property (e.g. Property:P2, Property:P25).
        """
        print(f"Fetching backlinks for Property:{property_id}...")
        qids: Set[str] = set()
        bltitle = f"Property:{property_id}"
        blcontinue = None

        while True:
            params: Dict[str, Any] = {
                "action": "query",
                "list": "backlinks",
                "bltitle": bltitle,
                "bllimit": 50
            }
            if blcontinue:
                params["blcontinue"] = blcontinue

            data = self._make_request(params)
            backlinks = data.get("query", {}).get("backlinks", [])
            for item in backlinks:
                title = item.get("title", "")
                if title.startswith("Item:Q"):
                    qids.add(title.replace("Item:", ""))

            if max_items and len(qids) >= max_items:
                break

            if "continue" in data and "blcontinue" in data["continue"]:
                blcontinue = data["continue"]["blcontinue"]
            else:
                break

        print(f"Discovered {len(qids)} unique Q-items for Property:{property_id}.")
        return sorted(list(qids), key=lambda x: int(x[1:]) if x[1:].isdigit() else 99999999)

    def fetch_entities(self, qids: List[str], chunk_size: int = 50) -> Dict[str, Any]:
        """
        Fetches detailed entity records (labels, descriptions, claims, aliases) for a list of QIDs.
        """
        entities: Dict[str, Any] = {}
        total = len(qids)
        print(f"Fetching {total} entity details from lgbtDB in batches of {chunk_size}...")

        for i in range(0, total, chunk_size):
            chunk = qids[i:i + chunk_size]
            params = {
                "action": "wbgetentities",
                "ids": "|".join(chunk),
                "props": "info|labels|descriptions|aliases|claims"
            }
            data = self._make_request(params)
            batch_entities = data.get("entities", {})
            for qid, ent in batch_entities.items():
                if "missing" not in ent:
                    entities[qid] = ent
            
            if (i // chunk_size) % 5 == 0 or (i + chunk_size) >= total:
                print(f"  Progress: {min(i + chunk_size, total)}/{total} entities fetched...")
            time.sleep(0.1)

        return entities

    def get_class_candidate_entities(
        self,
        max_classes: Optional[int] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Fetches all candidate classes from lgbtDB:
        - Entities with subclass of (P2)
        - Entities with GSSO V2 ID (P25)
        - Parent entities referenced in P2 (ensures closure)
        """
        if use_cache and os.path.exists(self.entities_cache_file):
            print(f"Loading cached lgbtDB entities from {self.entities_cache_file}...")
            with open(self.entities_cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if cached:
                print(f"Loaded {len(cached)} cached entities.")
                return cached

        # 1. Fetch QIDs using P2 (subclass of)
        p2_qids = self.fetch_property_backlinks(PROP_SUBCLASS_OF, max_items=max_classes)
        # 2. Fetch QIDs using P25 (GSSO V2 ID)
        p25_qids = self.fetch_property_backlinks(PROP_GSSO_V2_ID, max_items=max_classes)

        combined_qids = sorted(list(set(p2_qids + p25_qids)), key=lambda x: int(x[1:]) if x[1:].isdigit() else 99999999)
        if max_classes:
            combined_qids = combined_qids[:max_classes]

        # 3. Fetch full entity records
        entities = self.fetch_entities(combined_qids)

        # 4. Find any referenced parent QIDs from P2 that were not in combined_qids
        parent_qids: Set[str] = set()
        for ent in entities.values():
            claims = ent.get("claims", {})
            for snak in claims.get(PROP_SUBCLASS_OF, []):
                val = snak.get("mainsnak", {}).get("datavalue", {}).get("value", {})
                if isinstance(val, dict) and val.get("id"):
                    pid = val["id"]
                    if pid.startswith("Q") and pid not in entities:
                        parent_qids.add(pid)

        if parent_qids:
            print(f"Fetching {len(parent_qids)} additional parent entities for hierarchy closure...")
            parent_entities = self.fetch_entities(list(parent_qids))
            entities.update(parent_entities)

        # 5. Save to cache
        print(f"Saving {len(entities)} entities to cache: {self.entities_cache_file}")
        with open(self.entities_cache_file, "w", encoding="utf-8") as f:
            json.dump(entities, f, indent=2)

        return entities
