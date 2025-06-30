import requests
import xml.etree.ElementTree as ET

def is_valid_keyword(keyword):
    """Basic validation to check if keyword is a non-empty string"""
    return isinstance(keyword, str) and len(keyword.strip()) > 0

def fetch_papers_by_keyword(keyword, max_results=1):
    """
    Fetches research papers from PubMed by keyword.
    Returns a list of paper dicts (title, abstract, year, pmid).
    """
    if not is_valid_keyword(keyword):
        return {"error": "Invalid or empty keyword."}

    # Step 1: Use ESearch to get list of PubMed IDs (PMIDs)
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params = {
        "db": "pubmed",
        "term": keyword,
        "retmax": max_results,
        "retmode": "json"
    }

    try:
        esearch_resp = requests.get(esearch_url, params=esearch_params, timeout=10)
        if esearch_resp.status_code != 200:
            return {"error": f"ESearch API request failed with status {esearch_resp.status_code}"}
        esearch_data = esearch_resp.json()
        id_list = esearch_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return {"error": "No papers found for this keyword."}
    except Exception as e:
        return {"error": f"Exception during ESearch API request: {str(e)}"}

    # Step 2: Use EFetch to get details (title, abstract) for each PMID
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    efetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }

    try:
        efetch_resp = requests.get(efetch_url, params=efetch_params, timeout=10)
        if efetch_resp.status_code != 200:
            return {"error": f"EFetch API request failed with status {efetch_resp.status_code}"}
        
        # Parse XML response
        root = ET.fromstring(efetch_resp.text)
        results = []
        for article in root.findall(".//PubmedArticle"):
            title = article.findtext(".//ArticleTitle")
            abstract_text = ""
            abstract = article.find(".//Abstract")
            if abstract is not None:
                # Combine all abstract sections if multiple
                abstract_text = " ".join([elem.text for elem in abstract.findall("AbstractText") if elem.text])
            pub_year = article.findtext(".//PubDate/Year")
            pmid = article.findtext(".//PMID")
            
            results.append({
                "title": title if title else "",
                "abstract": abstract_text if abstract_text else "",
                "year": pub_year if pub_year else "",
                "id": pmid if pmid else ""
            })

        return results

    except Exception as e:
        return {"error": f"Exception during EFetch API request: {str(e)}"}
