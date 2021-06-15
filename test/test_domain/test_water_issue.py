from domain.water_issue import WaterIssue


def test_water_issue_create_from_dict():
    payload = {
        "date_text": "15.06.2021",
        "content": "useful content",
        "is_sent_telegram": True,
    }
    wi = WaterIssue.create_from_dict(payload)
    assert wi.date_text == "15.06.2021"
    assert wi.content == "useful content"
    assert wi.is_sent_telegram is True


def test_water_issue_create_from_empty_dict():
    payload = {}
    wi = WaterIssue.create_from_dict(payload)
    assert wi.date_text == ""
    assert wi.content == ""
    assert wi.is_sent_telegram is False
    assert wi.is_empty is True


def test_water_issue_hash():
    expected_hash = "eb8b5cb1f26c1f422a7ecc9f10cc97726bd487e15c83bab48678cc50d5e438d1"
    wi = WaterIssue(
        date_text="15.06.2021", content="useful content", is_sent_telegram=False
    )
    assert wi.hash == expected_hash

    wi_sent = WaterIssue(
        date_text="15.06.2021", content="useful content", is_sent_telegram=True
    )
    assert wi_sent.hash == expected_hash


def test_water_issue_formatted():
    wi = WaterIssue(date_text="15.06.2021", content="useful content")
    assert wi.formatted == "15.06.2021\n\nuseful content"


def test_water_issue_asdict():
    wi = WaterIssue(
        date_text="15.06.2021", content="useful content", is_sent_telegram=True
    )
    d = wi.asdict
    assert d["date_text"] == "15.06.2021"
    assert d["content"] == "useful content"
    assert d["is_sent_telegram"] is True


def test_water_issue_empty():
    wi = WaterIssue(date_text="15.06.2021", content=" ", is_sent_telegram=True)
    assert wi.is_empty is True
