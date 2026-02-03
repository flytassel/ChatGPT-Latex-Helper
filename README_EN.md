# ChatGPT Formula Clipboard Formatter

[中文版](./README.md)

A real-time clipboard listener built with Python, specifically designed to fix LaTeX formula formatting issues when copying from ChatGPT. It automatically converts the common bracketed block math `[` ... `]` into standard `$$ ... $$` format, while also handling inline math and redundant empty lines.

## Key Features

- **🚀 Real-time Listening**: Automatically monitors clipboard changes and performs instant conversions in the background.
- **📝 Block Math Conversion**: Automatically transforms formula blocks wrapped in `[` ... `]` into single-line `$$ ... $$`.
- **🔗 Inline Math Handling**: Intelligently identifies LaTeX content within `(...)` (e.g., containing `\`, `^`, `_`) and converts them to `$$ ... $$`.
- **🛡️ Nested Parentheses Support**: Perfectly handles complex mathematical expressions with nested parentheses like `(d_k(w))`.
- **📦 Quote Block Support**: Handles formula blocks preceded by `>` (common in ChatGPT quote replies).
- **🧹 Aggressive Cleanup**:
    - **Multi-line Merging**: Merges fragmented multi-line formulas into a clean single line.
    - **Zero Empty Lines**: Removes ALL empty lines from the text for a compact and consistent output.
- **🔒 Security Shield**: Built-in protection mechanism to prevent already converted formulas from being incorrectly processed again.

## Requirements

Ensure you have the `pyperclip` library installed for clipboard operations:

```bash
pip install pyperclip
```

## Usage

1. **Start the Script**:
   Run in your terminal:
   ```bash
   python format_formulas.py
   ```
2. **Copy Content**:
   Simply copy the reply content from ChatGPT in your browser.
3. **Automatic Conversion**:
   The script detects the change, processes it instantly, and updates your clipboard.
4. **Paste Anywhere**:
   Paste the content into your editor or document; all formulas will now be in standard LaTeX format.

## Example

### Input (ChatGPT Original):
```text
* Global Objective:
  [
  \min_w F(w) \triangleq \sum_{k=1}^K \frac{n_k}{n} G_k(w)
  ]

  where (\gamma_k^t) is a parameter.
```

### Output (Processed):
```text
* Global Objective:
  $$ \min_w F(w) \triangleq \sum_{k=1}^K \frac{n_k}{n} G_k(w) $$
  where $$ \gamma_k^t $$ is a parameter.
```

## Notes

- **Stop the Program**: Press `Ctrl + C` in the terminal to stop listening.
- **Permissions**: Ensure your terminal has permission to access the system clipboard.
- **Restart Required**: If you modify the `format_formulas.py` source code, you must restart the script to apply the changes.
