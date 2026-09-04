from fastapi import APIRouter, HTTPException, UploadFile, File
from pypdf import PdfReader
from io import BytesIO
import traceback

from app.ai.pipeline import analyze_proposal


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(file_bytes: bytes) -> str:

    reader = PdfReader(
        BytesIO(file_bytes)
    )

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    full_text = "\n".join(pages).strip()

    if not full_text:

        raise ValueError(
            "No readable text found in PDF."
        )

    return full_text


# ============================================================
# ANALYZE PDF
# ============================================================

@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...)
):

    print("\n" + "=" * 60)
    print("CSR PROPOSAL ANALYSIS STARTED")
    print("=" * 60)

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:

        # ----------------------------------------------------
        # Read PDF
        # ----------------------------------------------------

        print("STEP 1/4 - Reading PDF...")

        file_bytes = await file.read()

        if not file_bytes:

            raise ValueError(
                "Uploaded PDF is empty."
            )

        print(
            f"PDF size: {len(file_bytes)} bytes"
        )

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        print(
            "STEP 2/4 - Extracting PDF text..."
        )

        proposal_text = extract_text_from_pdf(
            file_bytes
        )

        print(
            f"Extracted characters: {len(proposal_text)}"
        )

        # ----------------------------------------------------
        # AI analysis
        # ----------------------------------------------------

        print(
            "STEP 3/4 - Running AI analysis..."
        )

        result = analyze_proposal(
            proposal_text
        )

        print(
            "STEP 4/4 - Analysis completed."
        )

        # ----------------------------------------------------
        # Add document information
        # ----------------------------------------------------

        result["document"] = {

            "filename": file.filename,

            "content_type": file.content_type,

            "text_length": len(proposal_text)
        }

        print("=" * 60)
        print("SUCCESS - CSR ANALYSIS COMPLETE")
        print("=" * 60)

        return result

    except HTTPException:

        raise

    except Exception as e:

        # ----------------------------------------------------
        # PRINT FULL ERROR
        # ----------------------------------------------------

        print("\n" + "=" * 60)
        print("!!! AI ANALYSIS ERROR !!!")
        print("=" * 60)

        print(
            f"ERROR TYPE: {type(e).__name__}"
        )

        print(
            f"ERROR MESSAGE: {str(e)}"
        )

        print("\nFULL TRACEBACK:")

        traceback.print_exc()

        print("=" * 60)

        raise HTTPException(

            status_code=500,

            detail=(
                f"AI analysis failed: "
                f"{type(e).__name__}: {str(e)}"
            )
        )