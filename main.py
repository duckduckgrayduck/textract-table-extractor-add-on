"""
Extract tables in documents on DocumentCloud using Amazon Textract
"""

import os
import sys
import csv
import zipfile
from PIL import Image
from textractor import Textractor
from textractor.visualizers.entitylist import EntityList
from textractor.data.constants import TextractFeatures, Direction, DirectionalFinderType
from documentcloud.addon import AddOn
from documentcloud.exceptions import APIError

class TableExtractor(AddOn):
    """Extract tables using Amazon Textract"""
    def calculate_cost(self, documents):
        """ Given a set of documents, counts the number of pages and returns a cost"""
        total_num_pages = 0
        for doc in documents:
            start_page = self.data.get("start_page", 1)
            end_page = self.data.get("end_page")
            last_page = 0
            if end_page <= doc.page_count:
                last_page = end_page
            else:
                last_page = doc.page_count
            pages_to_analyze = last_page - start_page + 1
            total_num_pages += pages_to_analyze
        cost = total_num_pages * 10
        print(cost)
        return cost

    def validate(self):
        """Validate that we can run the analysis"""

        if self.get_document_count() is None:
            self.set_message(
                "It looks like no documents were selected. Search for some or "
                "select them and run again."
            )
            sys.exit(0)
        if not self.org_id:
            self.set_message("No organization to charge.")
            sys.exit(0)
        ai_credit_cost = self.calculate_cost(
            self.get_documents()
        )
        try:
            self.charge_credits(ai_credit_cost)
        except ValueError:
            return False
        except APIError:
            return False
        return True

    def main(self):
        """The main add-on functionality goes here."""
        output_format = self.data.get("output_format", "csv")
        start_page = self.data.get("start_page", 1)
        end_page = self.data.get("end_page", 1)

        if not self.validate():
            self.set_message(
                "You do not have sufficient AI credits to run this Add-On on this document set"
            )
            sys.exit(0)

        if end_page < start_page:
            self.set_message("The end page you provided is smaller than the start page, try again")
            sys.exit(0)
        if start_page < 1:
            self.set_message("Your start page is less than 1, please try again")
            sys.exit(0)

        for document in self.get_documents():
            pass


if __name__ == "__main__":
    TableExtractor().main()
