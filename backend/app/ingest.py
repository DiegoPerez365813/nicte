"""Ingestion pipeline: download official Mexican legal PDFs, extract every
article automatically, and write them as structured JSON chunks the RAG
retriever can load.

This replaces hand-curated corpus files (app/legal_corpus/*.py, ~20
paraphrased articles) with the full, official text of each law (thousands
of articles), sourced directly from diputados.gob.mx (DOF-published PDFs).

Run manually (re-run when laws are amended):

    python -m app.ingest

Output: app/data/processed/{code}.json — one file per law, each a list of
chunk dicts with the same shape as app/legal_corpus/*.py entries, so the
retriever can merge both formats transparently.
"""

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import httpx
from pypdf import PdfReader

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

BOILERPLATE_PATTERNS = [
    r"Cámara de Diputados del H\. Congreso de la Unión",
    r"Secretaría General",
    r"Secretaría de Servicios Parlamentarios",
    r"Última Reforma DOF.*",
    r"^\d{1,4}\s*$",  # bare page numbers
    r"LeyesBiblio",
]


@dataclass
class LawSource:
    code: str
    law_name: str
    area: str
    jurisdiction: str
    url: str


SOURCES: list[LawSource] = [
    LawSource("CPEUM", "Constitución Política de los Estados Unidos Mexicanos", "constitucional", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf"),
    LawSource("LFT", "Ley Federal del Trabajo", "laboral", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf"),
    LawSource("CCF", "Código Civil Federal", "civil", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf"),
    LawSource("CPF", "Código Penal Federal", "penal", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPF.pdf"),
    LawSource("CCO", "Código de Comercio", "mercantil", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCom.pdf"),
    LawSource("CFF", "Código Fiscal de la Federación", "fiscal", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf"),
    LawSource("LGAMVLV", "Ley General de Acceso de las Mujeres a una Vida Libre de Violencia", "familiar", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/LGAMVLV.pdf"),
    LawSource("LFPDPPP", "Ley Federal de Protección de Datos Personales en Posesión de los Particulares",
               "derechos_humanos", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf"),

    # State codes — penal, civil and family law in Mexico are mostly state
    # jurisdiction, not federal. The federal codes above (CPF, CCF) only
    # govern federal-territory/federal-crime matters; most real disputes
    # are governed by the state where they happened. Starting with the four
    # most populous states; jurisdiction holds the state name so the
    # retriever can prefer a user's own state over others.
    LawSource("CPDF", "Código Penal para el Distrito Federal", "penal", "Ciudad de México",
               "https://data.consejeria.cdmx.gob.mx/images/leyes/codigos/2025/CODIGO_PENAL_PARA_EL_DF_12.3.2.pdf"),
    LawSource("CCDF", "Código Civil para el Distrito Federal", "civil", "Ciudad de México",
               "https://www.congresocdmx.gob.mx/media/documentos/50289a13825049361bb4abc0298d1374beed4009.pdf"),
    LawSource("CPJAL", "Código Penal para el Estado Libre y Soberano de Jalisco", "penal", "Jalisco",
               "https://transparencia.info.jalisco.gob.mx/sites/default/files/CODIGO%20PENAL%20PARA%20EL%20ESTADO%20DE%20JALISCO_2.pdf"),
    LawSource("CCJAL", "Código Civil del Estado de Jalisco", "civil", "Jalisco",
               "https://transparencia.info.jalisco.gob.mx/sites/default/files/C%C3%B3digo%20Civil%20del%20Estado%20de%20Jalisco_3.pdf"),
    LawSource("CPNL", "Código Penal para el Estado de Nuevo León", "penal", "Nuevo León",
               "https://www.linares.gob.mx/transparencia/95_01_normatividad/leyes_estatales/47_Codigo_Penal_Nuevo_Leon.pdf"),
    LawSource("CCNL", "Código Civil para el Estado de Nuevo León", "civil", "Nuevo León",
               "http://www.ordenjuridico.gob.mx/Publicaciones/DI2005/pdf/NL1.pdf"),
    LawSource("CPMEX", "Código Penal del Estado de México", "penal", "Estado de México",
               "https://legislacion.edomex.gob.mx/sites/legislacion.edomex.gob.mx/files/files/pdf/cod/vig/codvig006.pdf"),
    LawSource("CCMEX", "Código Civil del Estado de México", "civil", "Estado de México",
               "https://legislacion.edomex.gob.mx/sites/legislacion.edomex.gob.mx/files/files/pdf/cod/vig/codvig001.pdf"),

    # Remaining 28 states, completing all-32-state coverage.
    LawSource("CPAGS", "Código Penal para el Estado de Aguascalientes", "penal", "Aguascalientes",
               "https://congresoags.gob.mx/agenda_legislativa/leyes/descargarPdf/2481"),
    LawSource("CCAGS", "Código Civil del Estado de Aguascalientes", "civil", "Aguascalientes",
               "https://eservicios2.aguascalientes.gob.mx/NormatecaAdministrador/archivos/EDO-4-1.pdf"),
    LawSource("CPBC", "Código Penal para el Estado de Baja California", "penal", "Baja California",
               "https://transparencia.pjbc.gob.mx/documentos/pdfs/Codigos/CodigoPenal.pdf"),
    LawSource("CCBC", "Código Civil para el Estado de Baja California", "civil", "Baja California",
               "https://transparencia.pjbc.gob.mx/documentos/pdfs/Codigos/CodigoCivil.pdf"),
    LawSource("CPBCS", "Código Penal para el Estado Libre y Soberano de Baja California Sur", "penal", "Baja California Sur",
               "https://tribunalbcs.gob.mx/admin/imgDep/Tribunal/CodigoPenal/C%C3%B3digo%20Penal%20BCS%2024-04-2023.pdf"),
    LawSource("CCBCS", "Código Civil para el Estado Libre y Soberano de Baja California Sur", "civil", "Baja California Sur",
               "https://tribunalbcs.gob.mx/admin/imgDep/Tribunal/codigo%20civil/C%C3%B3digo%20Civil%20actualizado%20al%2020%20de%20Julio%20de%202022.pdf"),
    LawSource("CPCAM", "Código Penal del Estado de Campeche", "penal", "Campeche",
               "https://campeche.gob.mx/wp-content/uploads/2022/10/Codigo_Penal_del_Estado_de_Campeche.pdf"),
    LawSource("CCCAM", "Código Civil del Estado de Campeche", "civil", "Campeche",
               "https://transparenciafiscal.campeche.gob.mx/images/Documentos/Bloque%201/Codigo%20Civil%20del%20Estado%20de%20Campeche.pdf"),
    LawSource("CPCHIS", "Código Penal para el Estado de Chiapas", "penal", "Chiapas",
               "https://poderjudicialchiapas.gob.mx/storage/legislacion/0595CE33-5884-48EE-92CB-EC58FF38283A.pdf"),
    LawSource("CCCHIS", "Código Civil del Estado de Chiapas", "civil", "Chiapas",
               "https://poderjudicialchiapas.gob.mx/storage/legislacion/07EEACD0-560E-4497-A076-9ADE2D7864F8.pdf"),
    LawSource("CPCHIH", "Código Penal del Estado de Chihuahua", "penal", "Chihuahua",
               "https://chihuahua.gob.mx/atach2/justiciapenal/uploads/cod%20penal.pdf"),
    LawSource("CCCHIH", "Código Civil del Estado de Chihuahua", "civil", "Chihuahua",
               "https://www.congresochihuahua2.gob.mx/biblioteca/codigos/archivosCodigos/77.pdf"),
    LawSource("CPCOAH", "Código Penal del Estado de Coahuila de Zaragoza", "penal", "Coahuila",
               "https://www.congresocoahuila.gob.mx/transparencia/03/Leyes_Coahuila/coa08_Nuevo_Codigo.pdf"),
    LawSource("CCCOAH", "Código Civil para el Estado de Coahuila de Zaragoza", "civil", "Coahuila",
               "https://www.coahuilatransparente.gob.mx/codigos/documentos_codigos/CODIGO%20CIVIL%20PARA%20EL%20ESTADO.pdf"),
    LawSource("CPCOL", "Código Penal para el Estado de Colima", "penal", "Colima",
               "https://congresocol.gob.mx/web/Sistema/uploads/LegislacionEstatal/Codigos/codigo_penal_09sept2024.pdf"),
    LawSource("CCCOL", "Código Civil para el Estado de Colima", "civil", "Colima",
               "https://docs.mexico.justia.com/estatales/colima/codigo-civil-para-el-estado-de-colima.pdf"),
    LawSource("CPDGO", "Código Penal del Estado Libre y Soberano de Durango", "penal", "Durango",
               "https://congresodurango.gob.mx/Archivos/legislacion/CODIGO%20PENAL%20(NUEVO).pdf"),
    LawSource("CCDGO", "Código Civil del Estado de Durango", "civil", "Durango",
               "https://congresodurango.gob.mx/Archivos/legislacion/CODIGO%20CIVIL.pdf"),
    LawSource("CPGTO", "Código Penal del Estado de Guanajuato", "penal", "Guanajuato",
               "https://sistemaestatalanticorrupcion.guanajuato.gob.mx/wp-content/uploads/2021/07/CODIGO-PENAL-DEL-ESTADO-DE-GUANAJUATO.pdf"),
    LawSource("CCGTO", "Código Civil para el Estado de Guanajuato", "civil", "Guanajuato",
               "https://congreso-gto.s3.amazonaws.com/uploads/reforma/pdf/3596/CCG_REF_27Dic2024.pdf"),
    LawSource("CPGRO", "Código Penal para el Estado Libre y Soberano de Guerrero", "penal", "Guerrero",
               "https://www.guerrero.gob.mx/wp-content/uploads/2026/02/CPEGN499.pdf"),
    LawSource("CCGRO", "Código Civil del Estado Libre y Soberano de Guerrero", "civil", "Guerrero",
               "https://armonizacion.cndh.org.mx/Content/Files/LGBTTTI/CodCivilFam/13Codigo_CE_Gro.pdf"),
    LawSource("CPHGO", "Código Penal para el Estado de Hidalgo", "penal", "Hidalgo",
               "https://www.congreso-hidalgo.gob.mx/biblioteca_legislativa/leyes_cintillo/Codigo%20Penal%20para%20el%20Estado%20de%20Hidalgo.pdf"),
    LawSource("CCHGO", "Código Civil para el Estado de Hidalgo", "civil", "Hidalgo",
               "https://www.congreso-hidalgo.gob.mx/biblioteca_legislativa/leyes_cintillo/Codigo%20Civil.pdf"),
    LawSource("CPMICH", "Código Penal del Estado de Michoacán", "penal", "Michoacán",
               "https://michoacan.gob.mx/wp-content/uploads/2025/10/CO%CC%81DIGO-PENAL-DEL-ESTADO-DE-MICHOACA%CC%81N.pdf"),
    LawSource("CCMICH", "Código Civil para el Estado de Michoacán", "civil", "Michoacán",
               "http://ordenjuridico.gob.mx/Publicaciones/DI2005/pdf/MICH1.pdf"),
    LawSource("CPMOR", "Código Penal para el Estado de Morelos", "penal", "Morelos",
               "http://marcojuridico.morelos.gob.mx/archivos/codigos/pdf/CPENALEM.pdf"),
    LawSource("CCMOR", "Código Civil para el Estado Libre y Soberano de Morelos", "civil", "Morelos",
               "http://marcojuridico.morelos.gob.mx/archivos/codigos/pdf/CCIVILEM.pdf"),
    LawSource("CPNAY", "Código Penal para el Estado de Nayarit", "penal", "Nayarit",
               "https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/codigos/codigo_penal_nuevo.pdf"),
    LawSource("CCNAY", "Código Civil para el Estado de Nayarit", "civil", "Nayarit",
               "https://congresonayarit.gob.mx/wp-content/uploads/QUE_HACEMOS/LEGISLACION_ESTATAL/codigos/codigo_civil_estado_de_nayarit.pdf"),
    LawSource("CPOAX", "Código Penal para el Estado de Oaxaca", "penal", "Oaxaca",
               "https://www.congresooaxaca.gob.mx/docs66.congresooaxaca.gob.mx/legislacion_estatal/Codigo_Penal_para_el_Edo_de_Oax_(_Ref_dto_769_aprob_LXVI_Legis_18_sep_2025_PO_41_8a_secc_11_oct_2025).pdf"),
    LawSource("CCOAX", "Código Civil para el Estado de Oaxaca", "civil", "Oaxaca",
               "https://armonizacion.cndh.org.mx/Content/Files/DMVLV/CC/OAX-CC.pdf"),
    LawSource("CPPUE", "Código Penal del Estado Libre y Soberano de Puebla", "penal", "Puebla",
               "https://ojp.puebla.gob.mx/media/k2/attachments/Codigo_Penal_del_Estado_Libre_y_Soberano_de_Puebla_2EV_15122025.pdf"),
    LawSource("CCPUE", "Código Civil para el Estado Libre y Soberano de Puebla", "civil", "Puebla",
               "https://ieepuebla.org.mx/2017/Normatividad/Codigo_Civil_del_edo_libre_y_soberano_de_puebla_29032016.pdf"),
    LawSource("CPQRO", "Código Penal para el Estado de Querétaro", "penal", "Querétaro",
               "https://site.legislaturaqueretaro.gob.mx/CloudPLQ/InvEst/Codigos/COD-ID-07.pdf"),
    LawSource("CCQRO", "Código Civil del Estado de Querétaro", "civil", "Querétaro",
               "https://www.poderjudicialqro.gob.mx/biblio/leeDoc.php?cual=844&tabla=tbiblioteca_historial"),
    LawSource("CPQROO", "Código Penal para el Estado Libre y Soberano de Quintana Roo", "penal", "Quintana Roo",
               "https://juventud.qroo.gob.mx/wp-content/uploads/2024/08/CODIGO-PENAL-PARA-EL-ESTADO-LIBRE-Y-SOBERANO-DE-QUINTANA-ROO.pdf"),
    LawSource("CCQROO", "Código Civil para el Estado de Quintana Roo", "civil", "Quintana Roo",
               "https://documentos.congresoqroo.gob.mx/codigos/C2-XVII-31052023-20230608T145647-C1720220531062.pdf"),
    LawSource("CPSLP", "Código Penal para el Estado de San Luis Potosí", "penal", "San Luis Potosí",
               "https://armonizacion.cndh.org.mx/Content/Files/LGBTTTI/CodPenal/24Codigo_PE_SLP.pdf"),
    LawSource("CCSLP", "Código Civil para el Estado de San Luis Potosí", "civil", "San Luis Potosí",
               "https://armonizacion.cndh.org.mx/Content/Files/DMVLV/CC/SLP-CC.pdf"),
    LawSource("CPSIN", "Código Penal para el Estado de Sinaloa", "penal", "Sinaloa",
               "https://www.congresosinaloa.gob.mx/images/congreso/leyes/zip/codigo_penal_28-dic-2016.pdf"),
    LawSource("CCSIN", "Código Civil para el Estado de Sinaloa", "civil", "Sinaloa",
               "https://media.transparencia.sinaloa.gob.mx/uploads/files/105/codigo%20civil.pdf"),
    LawSource("CPSON", "Código Penal para el Estado de Sonora", "penal", "Sonora",
               "https://coespo.sonora.gob.mx/images/documentos/gepea/FunLegales/CODIGO_PENAL.pdf"),
    LawSource("CCSON", "Código Civil para el Estado de Sonora", "civil", "Sonora",
               "https://docs.mexico.justia.com/estatales/sonora/codigo-civil-del-estado-de-sonora.pdf"),
    LawSource("CPTAB", "Código Penal para el Estado de Tabasco", "penal", "Tabasco",
               "https://congresotabasco.gob.mx/wp-content/uploads/2026/05/Codigo-Penal-para-el-Estado-de-Tabasco-1.pdf"),
    LawSource("CCTAB", "Código Civil para el Estado de Tabasco", "civil", "Tabasco",
               "https://tsj-tabasco.gob.mx/resources/pdf/biblioteca/codigo_civil.pdf"),
    LawSource("CPTAMS", "Código Penal para el Estado de Tamaulipas", "penal", "Tamaulipas",
               "https://po.tamaulipas.gob.mx/wp-content/uploads/2020/08/Codigo_Penal.pdf"),
    LawSource("CCTAMS", "Código Civil para el Estado de Tamaulipas", "civil", "Tamaulipas",
               "http://po.tamaulipas.gob.mx/wp-content/uploads/2026/03/Codigo_Civil.pdf"),
    LawSource("CPTLAX", "Código Penal para el Estado Libre y Soberano de Tlaxcala", "penal", "Tlaxcala",
               "https://tsjtlaxcala.gob.mx/transparencia/Fracciones_a63/I/codigos/codigopenaltlaxcala.pdf"),
    LawSource("CCTLAX", "Código Civil para el Estado de Tlaxcala", "civil", "Tlaxcala",
               "https://armonizacion.cndh.org.mx/Content/Files/LGBTTTI/CodCivilFam/29Codigo_CE_Tlax.pdf"),
    LawSource("CPVER", "Código Penal para el Estado Libre y Soberano de Veracruz de Ignacio de la Llave", "penal", "Veracruz",
               "https://docs.mexico.justia.com/estatales/veracruz/codigo-penal-para-el-estado-libre-y-soberano-de-veracruz-de-ignacio-de-la-llave.pdf"),
    LawSource("CCVER", "Código Civil para el Estado de Veracruz de Ignacio de la Llave", "civil", "Veracruz",
               "https://www.legisver.gob.mx/leyes/LeyesPDF/CCIVIL07042025.pdf"),
    LawSource("CPYUC", "Código Penal del Estado de Yucatán", "penal", "Yucatán",
               "https://docs.mexico.justia.com/estatales/yucatan/codigo-penal-del-estado-de-yucatan.pdf"),
    LawSource("CCYUC", "Código Civil del Estado de Yucatán", "civil", "Yucatán",
               "https://congresoyucatan.gob.mx/storage/legislacion/codigos/ca9da342d9e6c5faf13d9e39e9ec6591_2022-06-10.pdf"),
    LawSource("CPZAC", "Código Penal para el Estado de Zacatecas", "penal", "Zacatecas",
               "https://www.asezac.gob.mx/pages/transparencia/fracc_i/codigo_penal_estado_zacatecas.pdf"),
    LawSource("CCZAC", "Código Civil del Estado de Zacatecas", "civil", "Zacatecas",
               "https://cgj.zacatecas.gob.mx/MJE/CODIGOS/C%C3%93DIGO%20CIVIL%20DEL%20ESTADO%20DE%20ZACATECA1.pdf"),
]

ARTICLE_PATTERN = re.compile(
    # \d+(\.\d+)? handles decimal article numbering used by some state codes
    # (e.g. Estado de México: "Artículo 1.1", "Artículo 1.5 Bis") in addition
    # to the plain \d+ numbering most federal/state codes use. The terminator
    # is optional and may include ° (degree sign) because older codes like
    # Veracruz's write "ARTICULO 1°" or even just "ARTICULO 10 " (no
    # punctuation at all) before the article body starts.
    r"Art[íi]culo\s+(\d+(?:\.\d+)?(?:\s*(?:Bis|Ter|Qu[aá]ter|Quinquies)\b)?(?:[-–]\w+)?)\s*(?:[.\-–°]\s*)?",
    re.IGNORECASE,
)


def download_pdf(source: LawSource) -> Path:
    raw_path = RAW_DIR / f"{source.code}.pdf"
    if raw_path.exists():
        return raw_path

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    # Some state government sites (e.g. consejeria.cdmx.gob.mx) serve an
    # incomplete certificate chain — acceptable to skip verification here
    # since these are one-time admin downloads from known official domains,
    # not user-facing requests.
    with httpx.Client(follow_redirects=True, timeout=60, verify=False) as client:
        resp = client.get(source.url, headers={"User-Agent": "Mozilla/5.0 (Nicte-Ingest/0.1)"})
        resp.raise_for_status()
        raw_path.write_bytes(resp.content)
    return raw_path


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        lines = text.split("\n")
        cleaned_lines = [
            line for line in lines
            if not any(re.search(p, line) for p in BOILERPLATE_PATTERNS)
        ]
        pages_text.append(" ".join(cleaned_lines))
    full_text = " ".join(pages_text)
    return re.sub(r"\s+", " ", full_text).strip()


def split_into_articles(full_text: str, max_chars: int = 1800) -> list[tuple[str, str]]:
    matches = list(ARTICLE_PATTERN.finditer(full_text))
    articles = []
    for i, match in enumerate(matches):
        article_number = match.group(1).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        body = full_text[start:end].strip()
        if len(body) > max_chars:
            body = body[:max_chars].rstrip() + "..."
        if len(body) < 20:  # noise / false-positive match
            continue
        articles.append((article_number, body))
    return articles


def build_chunks(source: LawSource, articles: list[tuple[str, str]]) -> list[dict]:
    today = date.today().isoformat()
    chunks = []
    seen_numbers: set[str] = set()
    for article_number, text in articles:
        dedup_key = f"{article_number}"
        if dedup_key in seen_numbers:
            continue
        seen_numbers.add(dedup_key)
        chunks.append({
            "id": f"{source.code.lower()}-art-{article_number}".replace(" ", "-"),
            "law_name": source.law_name,
            "jurisdiction": source.jurisdiction,
            "article_number": article_number,
            "effective_date": today,
            "source_url": source.url,
            "area": source.area,
            "text": text,
        })
    return chunks


def ingest_source(source: LawSource) -> int:
    pdf_path = download_pdf(source)
    full_text = extract_text(pdf_path)
    articles = split_into_articles(full_text)
    chunks = build_chunks(source, articles)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"{source.code}.json"
    out_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(chunks)


def main() -> None:
    for source in SOURCES:
        out_path = PROCESSED_DIR / f"{source.code}.json"
        if out_path.exists():
            print(f"[SKIP] {source.code} already processed", flush=True)
            continue
        try:
            count = ingest_source(source)
            print(f"[OK] {source.code} ({source.law_name}) -> {count} artículos", flush=True)
        except Exception as exc:  # noqa: BLE001 — one bad source must not stop the rest
            print(f"[FAIL] {source.code}: {exc}", flush=True)


if __name__ == "__main__":
    main()
