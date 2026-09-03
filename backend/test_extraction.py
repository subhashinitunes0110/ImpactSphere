from app.services.document_parser import extract_text_from_pdf
from app.ai.extraction import extract_project_information


PDF_PATH = "../data/raw/test_proposal.pdf"


def main():

    print("=" * 60)
    print("IMPACT SPHERE - AI PROPOSAL EXTRACTION")
    print("=" * 60)

    print("\nReading PDF...")

    text = extract_text_from_pdf(PDF_PATH)

    print(f"PDF characters extracted: {len(text)}")

    print("\nSending proposal to AI...")

    project = extract_project_information(text)

    print("\nSTRUCTURED PROJECT DATA")
    print("=" * 60)

    print(project.model_dump_json(indent=2))

    print("=" * 60)


if __name__ == "__main__":
    main()