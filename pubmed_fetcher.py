import requests
import xml.etree.ElementTree as ET
from typing import List, Optional
import os
import csv


class PubMedFetcher:
    """Class for interacting with the PubMed API and processing research papers."""

    def __init__(self, query: str):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.query = query
        self.ids: List[str] = []

    def fetch_paper_ids(self) -> List[str]:
        """Fetches paper IDs from PubMed based on the user query."""
        params = {
            'db': 'pubmed',
            'term': self.query,
            'retmode': 'xml',
            'retmax': '100'  # Limit the number of results for testing
        }
        response = requests.get(self.base_url, params=params)

        # Debugging: Print the response for analysis
        print("Response from PubMed API:", response.text)

        response.raise_for_status()  # Ensure the request was successful

        # Parse the XML response and extract PubMed IDs
        root = ET.fromstring(response.text)
        ids = [id_elem.text for id_elem in root.findall(".//Id")]

        if not ids:
            print("No paper IDs found.")
        return ids

    def fetch_paper_details(self, ids: List[str]) -> List[dict]:
        """Fetches paper details from PubMed for the given list of paper IDs."""
        details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        papers = []

        for paper_id in ids:
            params = {
                'db': 'pubmed',
                'id': paper_id,
                'retmode': 'xml'
            }
            response = requests.get(details_url, params=params)

            # Debugging: Print the response for analysis
            print(f"Fetching details for PubMed ID {paper_id}: {response.text}")

            response.raise_for_status()

            # Parse the XML response
            root = ET.fromstring(response.text)

            # Extract the paper title and publication date with checks
            title = root.find(".//ArticleTitle")
            title = title.text if title is not None else "No Title"

            pub_date = root.find(".//PubDate/Year")
            pub_date = pub_date.text if pub_date is not None else "No Date"

            authors = root.findall(".//Author")
            author_names = [
                f"{author.find('LastName').text} {author.find('ForeName').text}" if author.find(
                    'LastName') is not None and author.find('ForeName') is not None else "Unknown"
                for author in authors
            ]
            author_affiliations = [
                author.find("Affiliation").text if author.find("Affiliation") is not None else "No Affiliation"
                for author in authors
            ]
            corresponding_email = root.find(".//CorrespondingAuthor/Email")
            corresponding_email = corresponding_email.text if corresponding_email is not None else "No Email"

            # Non-academic and company affiliations
            non_academic_authors = []
            company_affiliations = set()

            for idx, affiliation in enumerate(author_affiliations):
                if "pharma" in affiliation.lower() or "biotech" in affiliation.lower():
                    company_affiliations.add(affiliation)
                elif "university" not in affiliation.lower() and "lab" not in affiliation.lower():
                    non_academic_authors.append(author_names[idx])

            paper = {
                'PubmedID': paper_id,
                'Title': title,
                'Publication Date': pub_date,
                'Non-academic Author(s)': "; ".join(non_academic_authors),  # Join authors with semicolon
                'Company Affiliation(s)': "; ".join(company_affiliations),  # Join affiliations with semicolon
                'Corresponding Author Email': corresponding_email,
            }

            papers.append(paper)

        return papers

    def save_to_csv(self, papers: List[dict], filename: Optional[str] = None):
        """Clears the CSV file (if exists) and saves the filtered papers to a new CSV file."""
        header = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)",
                  "Corresponding Author Email"]

        # Use a default name if filename is not provided
        filename = filename or 'papers.csv'

        # Clear the file if it already exists (overwrite mode)
        if os.path.exists(filename):
            os.remove(filename)  # Remove the file before writing new data

        # Now save the new results
        with open(filename, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for paper in papers:
                writer.writerow(paper)
            print(f"Results saved to {filename}")
