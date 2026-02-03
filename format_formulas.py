import pyperclip
import re
import sys
import time

def process_text(text):
    """
    Process text to convert bracketed formula blocks into single-line LaTeX format wrapped in $$.
    Also handles inline formulas in parentheses containing LaTeX syntax.
    """
    # 1. Quoted Block Math
    # Matches:
    # > [
    # > ...
    # > ]
    quoted_block_pattern = re.compile(r'(?m)^(\s*>\s*)\[\s*\r?\n([\s\S]*?)\r?\n\s*>\s*\]\s*$')
    
    def quoted_block_replacement(match):
        prefix = match.group(1) # e.g. "> "
        content_block = match.group(2)
        
        lines = content_block.splitlines()
        cleaned_lines = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith('>'):
                stripped = stripped[1:].strip()
            else:
                stripped = line.strip()
            if stripped:
                cleaned_lines.append(stripped)
        
        merged = ' '.join(cleaned_lines)
        return f'{prefix}$$ {merged} $$'

    text = quoted_block_pattern.sub(quoted_block_replacement, text)

    # 2. Standard Block Math
    # Matches:
    # [
    # ...
    # ]
    block_pattern = re.compile(r'(?m)^(\s*)\[\s*\r?\n([\s\S]*?)\r?\n\s*\]\s*$')
    
    def block_replacement(match):
        indent = match.group(1)
        content_block = match.group(2)
        
        lines = [line.strip() for line in content_block.splitlines()]
        lines = [line for line in lines if line]
        merged = ' '.join(lines)
        return f'{indent}$$ {merged} $$'

    text = block_pattern.sub(block_replacement, text)

    # 3. Inline Math
    # Protection mechanism: Temporarily replace existing $$...$$ blocks with placeholders
    # to avoid double-processing content inside them.
    placeholders = []
    
    def protect_math_blocks(match):
        placeholders.append(match.group(0))
        return f'__MATH_BLOCK_{len(placeholders)-1}__'

    # Regex to find $$ ... $$ blocks. 
    # Using non-greedy match. Handling potentially multiline if needed, but our previous steps made them single line.
    # However, let's be safe.
    math_block_pattern = re.compile(r'\$\$([\s\S]*?)\$\$')
    text = math_block_pattern.sub(protect_math_blocks, text)

    # Now process inline math on the protected text
    # Matches (...) containing LaTeX indicators like \, ^, _
    # Updated regex to handle one level of nested parentheses, e.g., (d_k(w))
    # Pattern explanation:
    # \(             Start with (
    # (              Start capturing group 1 (content)
    #   (?:          Start non-capturing group for alternation
    #     [^()]+     One or more non-parenthesis characters
    #     |          OR
    #     \([^()]*\) A nested parenthesized group with no internal parentheses
    #   )*           Repeat zero or more times
    # )              End capturing group 1
    # \)             End with )
    inline_pattern = re.compile(r'\(((?:[^()]+|\([^()]*\))*)\)')
    
    def inline_replacement(match):
        content = match.group(1)
        # Check for LaTeX indicators
        # We look for backslash, caret, or underscore which are typical in LaTeX math
        # Also ensure it's not a placeholder
        if '__MATH_BLOCK_' in content:
             return match.group(0)

        if any(char in content for char in ['\\', '^', '_']):
            return f'$$ {content} $$'
        return match.group(0)

    text = inline_pattern.sub(inline_replacement, text)

    # Restore placeholders
    for i, original_block in enumerate(placeholders):
        text = text.replace(f'__MATH_BLOCK_{i}__', original_block)

    # 4. Cleanup: Remove ALL empty lines
    # Split into lines, strip each line, and keep only non-empty lines
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join([line for line in lines if line])

    return text

def main():
    print("正在监听剪贴板")

    # Initialize last_content to None so we process the current clipboard immediately on startup
    last_content = None

    while True:
        try:
            # Check for clipboard updates
            # pyperclip.paste() might fail sometimes if clipboard is locked by another app
            current_content = pyperclip.paste()
            
            if current_content != last_content:
                # Content changed (or first run)
                if not current_content:
                    # Clipboard is empty (or cleared), just update last_content
                    last_content = current_content
                else:
                    # Process the new content
                    processed = process_text(current_content)
                    
                    if processed != current_content:
                        # Found patterns to fix
                        pyperclip.copy(processed)
                        last_content = processed # Update last_content to the processed version
                        print("检测到公式块，已自动转换并更新剪贴板 (Processed and updated clipboard).")
                    else:
                        # No patterns found, just update last_content
                        last_content = current_content
                        # print("剪贴板变化，但无匹配内容 (Changed, no match).") 
                        # Optionally print a heartbeat or debug info if needed
                        # print(".", end="", flush=True)

            time.sleep(0.5) 

            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n程序已停止 (Stopped).")
            break
        except Exception as e:
            # specific handling for clipboard access errors could be added here
            # generally just print and wait a bit
            print(f"发生错误 (Error): {e}")
            time.sleep(1)

if __name__ == '__main__':
    main()
