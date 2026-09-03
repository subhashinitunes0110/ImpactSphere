from app.services.document_parser import extract_text_from_pdf


PDF_PATH = "../data/raw/test_proposal.pdf"


def main():
    print("=" * 60)
    print("IMPACT SPHERE - PDF EXTRACTION TEST")
    print("=" * 60)

    try:
        text = extract_text_from_pdf(PDF_PATH)

        print("\nExtracted Proposal:\n")
        print(text)

        print("\n" + "=" * 60)
        print(f"Characters extracted: {len(text)}")
        print("=" * 60)

    except Exception as error:
        print("\nERROR:")
        print(error)


if __name__ == "__main__":
    main()