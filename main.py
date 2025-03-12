import argparse
import logging
from pubmed_fetcher import PubMedFetcher


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query")

    # Define command line arguments
    parser.add_argument('query', type=str, help="Query to search PubMed", nargs='?', default="pharmaceutical research")  # Default to "pharmaceutical research"
    parser.add_argument('-f', '--file', type=str, help="Output CSV filename", default=None)
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debugging output")

    # Parse arguments
    args = parser.parse_args()

    # Set up logging
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # If query is not provided, use the default one
    if not args.query:
        logger.info("No query provided, using default query: 'pharmaceutical research'")
        args.query = "pharmaceutical research"

    # Initialize PubMedFetcher with the query
    pubmed_fetcher = PubMedFetcher(args.query)

    # Fetch paper IDs based on the query
    try:
        paper_ids = pubmed_fetcher.fetch_paper_ids()
    except Exception as e:
        logger.error(f"An error occurred while fetching paper IDs: {e}")
        return

    if paper_ids:
        logger.info(f"Found {len(paper_ids)} paper(s).")

        # Fetch paper details for the retrieved IDs
        try:
            papers = pubmed_fetcher.fetch_paper_details(paper_ids)
        except Exception as e:
            logger.error(f"An error occurred while fetching paper details: {e}")
            return

        if papers:
            logger.info(f"Found {len(papers)} papers with valid details.")
            # Save the papers to a CSV file (or print to console if no filename specified)
            pubmed_fetcher.save_to_csv(papers, filename=args.file)
        else:
            logger.warning("No papers found with valid details.")
    else:
        logger.warning("No paper IDs found for the query. Please check your search terms.")


if __name__ == "__main__":
    main()
