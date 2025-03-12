import json
import logging
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from tqdm import tqdm


class OutputHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing OutputHandler")
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    def save_output(
        self, data: str, output_file: Optional[str], schema_file: Optional[str] = None
    ) -> None:
        self.logger.debug("Starting output save process")
        try:
            total_steps = 1 + (1 if schema_file else 0) + (1 if output_file else 0)
            result = None
            with tqdm(total=total_steps, desc="Processing output") as pbar:
                if schema_file:
                    self.logger.debug(f"Loading schema from {schema_file}")
                    with tqdm(total=2, desc="Validating schema") as schema_pbar:
                        with open(schema_file, "r") as f:
                            schema = json.load(f)
                        schema_pbar.update(1)

                        prompt = f"Format this content according to this json schema: {json.dumps(schema)}\nContent: {data}"
                        response = self.llm.invoke(
                            prompt, response_format={"type": "json_object"}
                        )
                        print(response.content)
                        result = json.loads(response.content)
                        schema_pbar.update(1)

                    self.logger.info("Data validated against schema successfully")
                    pbar.update(1)

                if output_file:
                    self.logger.debug(f"Saving output to {output_file}")
                    with open(output_file, "w") as f:
                        f.write(json.dumps(result, indent=2))
                    self.logger.info(f"Data successfully saved to {output_file}")
                    pbar.update(1)
                else:
                    self.logger.debug("No output file specified, printing to console")
                    print(json.dumps(result, indent=2))
                    self.logger.info("Data successfully printed to console")
                    pbar.update(1)

        except Exception as e:
            self.logger.error(f"Error saving output: {str(e)}")
            raise
