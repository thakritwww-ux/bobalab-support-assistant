from app.dataset import build_pairs, development_examples


def test_all_pairs_and_split_isolation():
    pairs = build_pairs()
    assert len(pairs) == 128
    assert len({p["id"] for p in pairs}) == 128
    selected = development_examples(12)
    assert len(selected) == 12
    assert {p["split"] for p in selected} == {"development"}
    assert len({p["contact_id"] for p in selected[:8]}) == 8


def test_outbound_opener_is_history_not_a_customer_example():
    pair = next(p for p in build_pairs() if p["contact_id"] == "SYNTH_012")
    assert pair["chatHistory"][0]["role"] == "consultant"
    assert pair["client_message_ids"] == [2]
    assert len(pair["chatHistory"]) == 1


def test_sequences_attachments_and_delayed_event():
    pairs = {p["id"]: p for p in build_pairs()}
    assert pairs["SYNTH_008:7"]["client_message_ids"] == [7, 8]
    urgent = pairs["SYNTH_015:11"]
    assert urgent["client_message_ids"] == [11, 12, 13, 14]
    assert urgent["clientSequence"].count("[Non-text message]") == 3
    later = pairs["SYNTH_015:18"]
    assert later["consultant_message_ids"] == [19, 20]
    assert later["external_event_message_ids"] == [20]
    assert "UPDATE:" not in later["learningReference"]
    assert "UPDATE:" in later["consultantReply"]


def test_history_never_contains_current_customer_sequence():
    pair = build_pairs()[0]
    assert pair["chatHistory"] == []
    second = build_pairs()[1]
    assert len(second["chatHistory"]) == 2
    assert second["chatHistory"][-1]["role"] == "consultant"
