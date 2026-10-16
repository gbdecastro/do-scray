from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import re

class PublicationType(str, Enum):
    EDITION = "EDITION"
    CALL = "CALL"
    NOTICE = "NOTICE"
    BULLETIN = "BULLETIN"
    OTHER = "OTHER"

@dataclass(frozen=True)
class CanonicalDocument:
    key: str
    role: str
    url: str

@dataclass(frozen=True)
class CanonicalPublication:
    source_id: str
    key: str
    type: PublicationType
    title: str
    url: str
    documents: tuple[CanonicalDocument, ...]

def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    if p.scheme not in ("http", "https") or not p.netloc:
        raise ValueError("invalid URL")
    query = urlencode(sorted((k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith("utm_")))
    return urlunparse((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/") or "/", "", query, ""))

def canonicalize_edition(source_id: str, number: str, title: str, url: str, series: str | None = None) -> CanonicalPublication:
    if not re.fullmatch(r"\d+", number):
        raise ValueError("edition number must be numeric")
    key = f'edition:{series + ":" if series else ""}{int(number)}'
    url = normalize_url(url)
    return CanonicalPublication(source_id, key, PublicationType.EDITION, title, url, (CanonicalDocument("main", "MAIN", url),))

def canonicalize_cismetro(url: str, title: str, official_id: str | None = None) -> CanonicalPublication:
    url = normalize_url(url)
    drive = re.search(r"/file/d/([A-Za-z0-9_-]+)", url)
    if official_id:
        key = "call:" + official_id
    elif drive:
        key = "drive:" + drive.group(1)
    else:
        # Provisional: changing a URL may change the identity.
        key = "url:" + url
    return CanonicalPublication("cismetro", key, PublicationType.CALL, title, url, (CanonicalDocument("main", "MAIN", url),))

def validate_manifest(publication: CanonicalPublication) -> None:
    if not publication.source_id or not publication.key or not publication.title:
        raise ValueError("missing canonical identity")
    if not publication.documents:
        raise ValueError("publication must have documents")
    if len({d.key for d in publication.documents}) != len(publication.documents):
        raise ValueError("duplicate document key")
    normalize_url(publication.url)
    for document in publication.documents:
        if not document.key or document.role not in {"MAIN", "SUPPLEMENT", "ANNEX", "OTHER"}:
            raise ValueError("invalid document")
        normalize_url(document.url)
