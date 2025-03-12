import argparse
import json
import logging
from src.extract_10k import DocumentProcessor, OutputHandler
from dotenv import load_dotenv

load_dotenv()


def setup_logging(verbose_level):
    log_level = logging.WARNING
    if verbose_level == 1:
        log_level = logging.INFO
    elif verbose_level >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Extract sections from SEC 10k documents"
    )
    parser.add_argument("-u", "--url", required=True, help="Document URL or path")
    parser.add_argument(
        "-t", "--target", required=True, help="Target section to extract"
    )
    parser.add_argument("-s", "--schema", help="Output schema file")
    parser.add_argument("-o", "--output", help="Output JSON file")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (e.g., -v or -vv)",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    logger.info("Initializing document processor and output handler")
    doc_processor = DocumentProcessor()
    output_handler = OutputHandler()

    logger.info(f"Downloading and converting document from: {args.url}")
    document_data = doc_processor.download_and_convert_document(args.url)

    logger.info("Creating document chunks")
    chunks = doc_processor.create_chunks(document_data)

    logger.info("Creating vector store")
    vector_store = doc_processor.create_vector_store(chunks)

    logger.info(f"Finding relevant sections for target: {args.target}")
    relevant_sections = doc_processor.find_relevant_sections(vector_store, args.target)

    logger.info("Extracting target section")
    result = doc_processor.extract_target_section(relevant_sections, args.target)

    logger.info("Saving output")
    output_handler.save_output(result, args.output, args.schema)
    logger.info("Process completed successfully")


if __name__ == "__main__":
    main()
