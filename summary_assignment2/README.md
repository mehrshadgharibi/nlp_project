# Summary Maker - Assignment 2

## Overview
this project summarizes text in a specific style which is defined by the user.
if the text is too long hierarchical summarization is required.

## Features
- Measures document lengths and computes proportional target lengths
- Handles texts exceeding context window limits  which is 4000 tokens
- Implements hierarchical summarization for long documents:
  - Slicing documents into manageable chunks
  - Progressive summarization until fitting within context window
  - Style adaptation based on reference text

## Requirements
### Python Version:
- Python 3.11+
- NLTK library
   ```python
   pip install -r requirements.txt
   ```

## Usage
1. Prepare your input documents:

   - Text to be summarized (content_text.txt)
   - Reference text (style.txt)

2. Run the summarizer:
   ```python
   python main.py --reference content_text.txt --input style.txt --output styled_summary.txt
   ```

## Implementation Details
The summarization pipeline follows these steps:
1. Measure lengths of both documents
2. Compute proportional target lengths
3. For documents exceeding context window:
   - Slice into manageable chunks
   - Summarize each chunk
   - Collate summaries
   - Repeat summarization if needed
4. Generate final summary according to wanted style
5. Save output text