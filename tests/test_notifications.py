from services.notifications import app as notifications_app


def test_send_confirmation_returns_true():
    assert notifications_app.send_confirmation("ord_6", "customer@example.com") is True
