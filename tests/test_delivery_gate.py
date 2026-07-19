import os
import sys

_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo_root in sys.path:
    sys.path.remove(_repo_root)
sys.path.insert(0, _repo_root)

from delivery_gate import check_header_text


def test_header_order_passes():
    text = "Lakeville, MN | TroyHokanson@iCloud.com | linkedin.com/in/troyhokanson | TroyHokanson.com"
    assert check_header_text(text) == []


def test_missing_portfolio_fails():
    failures = check_header_text("Lakeville, MN | linkedin.com/in/troyhokanson")
    assert any("TroyHokanson.com" in item for item in failures)


def test_portfolio_before_linkedin_fails():
    failures = check_header_text("TroyHokanson.com | linkedin.com/in/troyhokanson")
    assert any("after LinkedIn" in item for item in failures)
