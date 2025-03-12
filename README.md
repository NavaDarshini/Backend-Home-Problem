# PubMed Paper Fetcher

## Overview

The **PubMed Paper Fetcher** is a Python application that interacts with the **PubMed API** to fetch research papers based on a user-specified query. The program filters papers to identify authors affiliated with pharmaceutical or biotech companies and saves the results to a CSV file. This tool is useful for researchers, developers, and anyone looking to automate the process of collecting academic papers from PubMed.

---

## How the Code is Organized

The project is divided into the following files:

1. **`pubmed_fetcher.py`**:
   - This is the core module that interacts with the PubMed API. It handles:
     - Fetching paper IDs based on the query.
     - Retrieving paper details, including title, authors, publication date, and author affiliations.
     - Filtering authors based on their affiliations (pharmaceutical or biotech companies).
     - Saving the filtered results to a CSV file.

2. **`main.py`**:
   - The main command-line interface (CLI) script that allows users to:
     - Input search queries.
     - Choose whether to save the results to a CSV file.
     - Enable debugging mode for detailed logs.

---

## Project Setup and Installation

### Prerequisites

To run this project, ensure that the following are installed on your system:

1. **Python 3.x** (preferably Python 3.7 or above).
   - You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

2. **Poetry** for dependency management and packaging (Optional but recommended).
   - Install Poetry: [Poetry Installation Guide](https://python-poetry.org/docs/#installation).

---

### Steps to Setup

1. **Clone the repository**:
   - Clone the project to your local machine using Git.

   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
# Backend-Home-Problem
