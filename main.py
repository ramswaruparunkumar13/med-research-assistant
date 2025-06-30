from fetch import fetch_papers_by_keyword
from summarise import generate_summary
from db import SemanticPaperDB  # Updated class name

MIN_ABSTRACT_LENGTH = 100  # Minimum valid abstract length

def main():
    db = SemanticPaperDB()  # Instantiate the new class

    while True:
        keyword = input("Enter a healthcare keyword to search papers or 'exit': ").strip()
        if keyword.lower() == 'exit':
            print("Exiting.")
            break

        papers = fetch_papers_by_keyword(keyword, max_results=3)
        if "error" in papers:
            print(f"Error fetching papers: {papers['error']}")
            continue

        # Filter out already-stored papers
        new_papers = [
            p for p in papers
            if len(p.get("abstract", "").strip()) >= MIN_ABSTRACT_LENGTH
            and not any(item["paper_id"] == p["id"] for item in db.metadata)
        ]

        valid_paper = new_papers[0] if new_papers else None

        if not valid_paper:
            # No new valid paper found – check DB for this keyword
            matched = [
                paper for paper in db.metadata
                if keyword.lower() in paper["summary"].lower() or keyword.lower() in paper["title"].lower()
            ]

            if matched:
                print("No new paper found, but here are some from your existing database:")
                for idx, entry in enumerate(matched, 1):
                    print(f"{idx}. {entry['title']} ({entry['year']})")

                choice = input("Enter the number of a paper to view its summary, or press Enter to skip: ").strip()
                if choice.isdigit():
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(matched):
                        selected = matched[choice_idx]
                        print(f"\nSummary for: {selected['title']} ({selected['year']})")
                        print(selected['summary'])
                    else:
                        print("Invalid selection.")
                else:
                    print("Skipping selection.")
            else:
                print("No suitable paper found in PubMed or in your database.")
            continue

        # Summarize and store the valid paper
        title = valid_paper.get("title", "No Title")
        year = valid_paper.get("year", "Unknown Year")
        paper_id = valid_paper.get("id", "No ID")
        abstract = valid_paper.get("abstract", "")

        print(f"\nSummarizing paper: {title} ({year})")

        summary = generate_summary(abstract)

        print("\nSummary:")
        print(summary)

        db.add_paper(paper_id, summary, title=title, year=year)

        # Show related papers
        similar = db.search_similar_by_paper_id(paper_id, k=2)
        if similar:
            print("\nRelated papers based on summary similarity:")
            for sim in similar:
                print(f"- {sim['title']} ({sim['year']})")
        else:
            print("\nNo similar papers found in the database.")

if __name__ == "__main__":
    main()
