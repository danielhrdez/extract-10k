# SEC 10k Extractor

This project is a extractor for financial documents in the public market companies like in the companies in the NASDAQ, SP500, ...

It takes url (or path) as input of the document and the target

```bash
uv run main.py --url https://example.com/amazon.pdf --target "Accounting Policies"
```

You can put to output directly to JSON:

```bash
uv run main.py --url https://example.com/amazon.pdf --target "Accounting Policies" --schema schema.json --output accounting_policies.json
```

| Parameters | Description |
| --- | --- |
| -u, --url | Document url or path |
| -t, --target | Search Term |
| -s, --schema | Output Schema |
| -o, --output | Output json file |

## Searching the target section

### Method 1 (Agentic AI)

1. Downloads the document.
2. Iteratively pass the first N words to the LLM asking "is this the section we are targetting?" and the model should output ONLY: {"success": boolean}. If it fails, then we pass the next N words, until we have hitted the target title.
3. with the section, output all of the [target] section into json with a predefined schema.

### Method 2 (MCP Agent)

1. Connect with playwright MCP the LLM to a browser.
2. Then get the document in the browser.
3. The model will search the target term iteratively taking screenshots until it's found.
4. with the section, output all of the [target] section into json with a predefined schema.

### Method 3 (Deterministic)

1. Downloads the document.
2. Search for the target in the document, then ask the LLM if this is the starts of the target section.
3. with the section, output all of the [target] section into json with a predefined schema.

### Method 4 (Greedy)

1. Downloads the document.
2. Calculate the tokens of the document, if it's less then N (128k for exmaple), then pass the entire document to the LLM.
3. with the section, output all of the [target] section into json with a predefined schema.

### Method 5 (Retrieval - RAG)

1. Downloads the document.
2. Divide the document into different chunks of text (each page for example) and get the embeddings.
3. Query the target section into the embeddings (vector search), the highest scored chunk will be passed to the LLM and ask to the LLM if this section fits (then pass the next section to check if the next chunk fit still on the target section).
4. with the section, output all of the [target] section into json with a predefined schema.

### Method 6 (Summary based - RAG)

1. Downloads the document.
2. Divide the document into different chunks of text (each page for example) and make a summary.
3. Query the target section into the summaries (semantic search), the highest scored chunk will be passed to the LLM and ask to the LLM if this section fits (then pass the next section to check if the next chunk fit still on the target section).
4. with the section, output all of the [target] section into json with a predefined schema.
