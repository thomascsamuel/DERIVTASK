# src/reporting_util.py

import logging
from datetime import datetime

def setup_logging(log_file='test.log'):
    """Sets up logging configuration."""
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def log_test_result(test_name, result):
    """Logs the result of a test case."""
    if result:
        logging.info(f"Test '{test_name}' passed.")
    else:
        logging.error(f"Test '{test_name}' failed.")

def generate_report(report_file='reports/test_reports.html'):
    """Generate a test report."""
    # This is a placeholder for report generation logic
    # You can use libraries like Jinja2 for HTML templates or just write HTML strings
    with open(report_file, 'w') as f:
        f.write("<html><body><h1>Test Report</h1>")
        f.write(f"<p>Report generated on {datetime.now()}</p>")
        f.write("</body></html>")
