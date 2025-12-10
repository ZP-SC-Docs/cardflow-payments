from app.payments import tokenise_card

SAMPLE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQyLCJlbWFpbCI6ImZpbmFuY2VAa2Vzc2lrLmV4YW1wbGUiLCJpYXQiOjE3MzA0NTYwMDB9.Qm9ndXNTaWduYXR1cmVGb3JGaXh0dXJlVXNlT25seTAwMDAw"


def test_tokenise_is_deterministic():
    assert tokenise_card("4111111111111111") == tokenise_card("4111111111111111")


def test_tokenise_differs_by_pan():
    assert tokenise_card("4111111111111111") != tokenise_card("5500000000000004")
