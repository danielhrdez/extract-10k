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

### Method 1 (Simple)

#### The largest PDF in the examples is the Apple 10-k which have 90k tokens (now every SOTA model have at least 128k context window)

1. Downloads the document.
2. Fit the entire document to the context window of the model
3. Query the model.

### Method 2 (Agentic AI)

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

## Results

Using method 1, there are some fail cases but 90% of the fields are covered in the documents. In this case it's better to improve the prompts for the models or use a beter model.

The cost per document processing is approximately $0.1, calculated as follows:

\[
\begin{aligned}
\text{Cost} &= (60{,}000 \times 1.1 \times 10^{-6}) + (10{,}000 \times 4.4 \times 10^{-6}) \\
&+ (10{,}000 \times 0.15 \times 10^{-6}) + (2{,}000 \times 0.6 \times 10^{-6}) \\
&= 0.066 + 0.044 + 0.0015 + 0.0012 \\
&= 0.1127 \text{ USD per document}
\end{aligned}
\]

Total cost = $0.1127
