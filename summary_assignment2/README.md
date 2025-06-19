

# Summary Maker - Assignment 2

## Overview
This project summarizes text in a specific style defined by the user.  
If the text is too long, hierarchical summarization is applied.

## Features
- Measures document lengths and computes proportional target lengths
- Handles texts exceeding the context window limit (4000 tokens)
- Implements hierarchical summarization for long documents:
  - Slices documents into manageable chunks
  - Applies progressive summarization until the content fits within the context window
  - Adapts summary style based on a reference text

## Requirements

### Python Version
- Python 3.11+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. Prepare your input documents:
   - `content_text.txt`: Text to be summarized
   - `style.txt`: Reference text for style

2. Run the summarizer:
   ```bash
   python main.py --reference style.txt --input content_text.txt --output styled_summary.txt
   ```

## Implementation Details

The summarization pipeline follows these steps:
1. Measure lengths of both documents
2. Compute proportional target lengths
3. For documents exceeding the context window:
   - Slice into manageable chunks
   - Summarize each chunk
   - Collate summaries
   - Repeat summarization if needed
4. Generate final summary according to the desired style
5. Save the output text

## Project Structure

```
summary-maker/
├── main.py                  # Entry point for running the summarizer
├── summarizer/
│   ├── __init__.py
│   ├── chunker.py           # Handles slicing of long documents
│   ├── summarizer.py        # Core summarization logic
│   ├── style_adapter.py     # Adapts summary to match reference style
│   └── utils.py             # Utility functions (e.g., token counting)
├── data/
│   ├── content_text.txt     # Input text to be summarized
│   ├── style.txt            # Reference style text
│   └── styled_summary.txt   # Output summary
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---