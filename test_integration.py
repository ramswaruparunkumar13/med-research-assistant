import tempfile
import os
import pytest
from summarise import generate_summary
from db import SemanticPaperDB

def test_generate_summary_basic():
    text = (
        "This study investigates the effects of a new drug on blood pressure in adults aged 40-65. "
        "A randomized controlled trial with 200 participants was conducted. "
        "Results show a significant decrease in systolic pressure with minimal side effects."
    )
    summary = generate_summary(text)
    assert isinstance(summary, str)
    assert len(summary) > 20
    assert "blood pressure" in summary.lower() or "drug" in summary.lower()

def test_semantic_paper_db_add_search():
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "test_index.faiss")
        metadata_path = os.path.join(tmpdir, "test_metadata.json")

        db = SemanticPaperDB(embedding_file=index_path, metadata_file=metadata_path)

        # DB should start empty
        assert len(db.metadata) == 0
        assert db.index.ntotal == 0

        # Add a couple of papers
        db.add_paper("paper1", "Summary of paper one about cardiovascular health.", "Cardio Health", "2023")
        db.add_paper("paper2", "Summary of paper two focusing on diabetes treatment.", "Diabetes Study", "2024")

        assert len(db.metadata) == 2
        assert db.index.ntotal == 2

        # Search test - should find relevant paper(s)
        results = db.search("cardiovascular research", k=2)
        assert any(r["paper_id"] == "paper1" for r in results)

        # Similar paper search
        similar = db.search_similar_by_paper_id("paper1", k=1)
        assert len(similar) == 1
        assert similar[0]["paper_id"] != "paper1"

if __name__ == "__main__":
    pytest.main([__file__])


