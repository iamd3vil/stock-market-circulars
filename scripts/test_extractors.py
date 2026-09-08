import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extractors import RSSExtractor


class MCXCircularsParserTest(unittest.TestCase):
    def test_parses_direct_pdf_links_and_deduplicates_category_tables(self):
        page = """
        <html><body>
          <table>
            <tr><th>Date</th><th>Category</th><th>Title</th><th>Circular No.</th></tr>
            <tr>
              <td>04 Sep 2026</td><td>T&amp;S</td>
              <td><a href="/docs/default-source/circulars/english/2026/september/circular---504---2026.pdf?sfvrsn=one">
                Extension of Implementation
              </a></td><td>504</td>
            </tr>
            <tr>
              <td>04 Sep 2026</td><td>T&amp;S</td>
              <td><a href="/docs/default-source/circulars/english/2026/september/circular---504---2026.pdf?sfvrsn=two">
                Extension of Implementation
              </a></td><td>504</td>
            </tr>
          </table>
          <a href="/unrelated-document.pdf">No circular date</a>
        </body></html>
        """

        items = RSSExtractor().parse_rss_feed(page, "mcx")

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Extension of Implementation")
        self.assertEqual(items[0]["pubdate"], "2026-09-04T00:00:00+05:30")
        self.assertEqual(
            items[0]["guid"],
            "https://www.mcxindia.com/docs/default-source/circulars/english/2026/september/circular---504---2026.pdf",
        )
        self.assertTrue(items[0]["download_url"].endswith("?sfvrsn=one"))


if __name__ == "__main__":
    unittest.main()
