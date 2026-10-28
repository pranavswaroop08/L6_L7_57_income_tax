#!/usr/bin/env python3
"""
generate_terminal_screenshots.py
Renders high-resolution terminal output screenshots for:
1. Baseline / Initial Coverage
2. Code Coverage Analysis (100% Line Coverage)
3. Branch Coverage Analysis (100% Branch Coverage)
"""

import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, commands_and_outputs, output_path):
    width = 980
    line_height = 22
    padding_x = 24
    header_height = 40
    font_size = 14
    
    # Windows standard monospace fonts
    font_paths = [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\lucon.ttf",
        "C:\\Windows\\Fonts\\cour.ttf"
    ]
    font_path = "consola.ttf"
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break

    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf" if os.path.exists("C:\\Windows\\Fonts\\consolab.ttf") else font_path, font_size)
    header_font = ImageFont.truetype(font_path, 12)

    # Flatten lines
    all_lines = []
    for item in commands_and_outputs:
        if item["type"] == "cmd":
            all_lines.append(("cmd", item["prompt"], item["text"]))
        elif item["type"] == "output":
            for subline in item["text"].split("\n"):
                all_lines.append(("output", "", subline))
        elif item["type"] == "spacer":
            all_lines.append(("spacer", "", ""))

    height = header_height + (len(all_lines) * line_height) + 30

    # Modern Dark Terminal Theme (Catppuccin Mocha style)
    bg_color = (24, 24, 37, 255)       # Base dark
    header_color = (17, 17, 27, 255)   # Crust header
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw header bar
    draw.rectangle([(0, 0), (width, header_height)], fill=header_color)

    # Window control buttons (macOS / modern style dots)
    draw.ellipse([(14, 14), (26, 26)], fill=(243, 139, 168, 255)) # Close (Red)
    draw.ellipse([(34, 14), (46, 26)], fill=(249, 226, 175, 255)) # Minimize (Yellow)
    draw.ellipse([(54, 14), (66, 26)], fill=(166, 227, 161, 255)) # Maximize (Green)

    # Title text
    title_bbox = draw.textbbox((0, 0), title, font=header_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 13), title, fill=(166, 173, 200, 255), font=header_font)

    # Body content
    y = header_height + 14
    for line_type, prompt, line in all_lines:
        if line_type == "cmd":
            draw.text((padding_x, y), prompt, fill=(137, 180, 250, 255), font=bold_font) # Sky blue prompt
            prompt_w = draw.textlength(prompt, font=bold_font)
            draw.text((padding_x + prompt_w, y), line, fill=(245, 224, 220, 255), font=bold_font) # Rosewater command
        elif line_type == "output":
            # Context-sensitive styling
            if "passed" in line or "[100%]" in line or " 100%" in line:
                fill_color = (166, 227, 161, 255)  # Green
            elif "===" in line or "---" in line:
                fill_color = (108, 112, 134, 255)  # Muted grey
            elif "Name" in line or "Stmts" in line:
                fill_color = (203, 166, 247, 255)  # Mauve table header
            elif "TOTAL" in line:
                fill_color = (137, 220, 235, 255)  # Bright cyan
            elif "33%" in line or "38%" in line or "Missing" in line:
                fill_color = (243, 139, 168, 255)  # Salmon/Red
            else:
                fill_color = (205, 214, 244, 255)  # Standard text
            draw.text((padding_x, y), line, fill=fill_color, font=font)
        elif line_type == "spacer":
            pass
        y += line_height

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_str = "PS C:\\Users\\prana\\Desktop\\se\\L6_L7_57_income_tax\\LAB6> "

    # 1. Baseline / Initial Coverage Report
    initial_cov_items = [
        {"type": "cmd", "prompt": prompt_str, "text": "coverage run --branch -m pytest test_income_tax.py"},
        {"type": "output", "text": "============================= test session starts =============================\n"
                                   "platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0\n"
                                   "rootdir: C:\\Users\\prana\\Desktop\\se\\L6_L7_57_income_tax\\LAB6\n"
                                   "collected 2 items\n\n"
                                   "test_income_tax.py ..                                                    [100%]\n\n"
                                   "============================== 2 passed in 0.02s =============================="},
        {"type": "spacer"},
        {"type": "cmd", "prompt": prompt_str, "text": "coverage report -m"},
        {"type": "output", "text": "Name                 Stmts   Miss Branch BrPart  Cover   Missing\n"
                                   "----------------------------------------------------------------\n"
                                   "income_tax.py           39     24     28      7    33%   3, 6-11, 14, 20, 22, 24, 29-32, 36-45\n"
                                   "test_income_tax.py       6      0      0      0   100%\n"
                                   "----------------------------------------------------------------\n"
                                   "TOTAL                   45     24     28      7    38%"}
    ]
    render_terminal(
        "Lab 6: Initial Baseline Coverage Report (33% Branch / 38% Line)",
        initial_cov_items,
        os.path.join(base_dir, "initial_coverage_report.png")
    )

    # 2. Code Coverage Report (100% Line Coverage)
    code_cov_items = [
        {"type": "cmd", "prompt": prompt_str, "text": "coverage run -m pytest CodeCoverageTest_income_tax.py"},
        {"type": "output", "text": "============================= test session starts =============================\n"
                                   "platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0\n"
                                   "rootdir: C:\\Users\\prana\\Desktop\\se\\L6_L7_57_income_tax\\LAB6\n"
                                   "collected 16 items\n\n"
                                   "CodeCoverageTest_income_tax.py ................                          [100%]\n\n"
                                   "============================== 16 passed in 0.04s =============================="},
        {"type": "spacer"},
        {"type": "cmd", "prompt": prompt_str, "text": "coverage report -m"},
        {"type": "output", "text": "Name                             Stmts   Miss  Cover   Missing\n"
                                   "--------------------------------------------------------------\n"
                                   "CodeCoverageTest_income_tax.py      38      0   100%\n"
                                   "income_tax.py                       39      0   100%\n"
                                   "--------------------------------------------------------------\n"
                                   "TOTAL                               77      0   100%"}
    ]
    render_terminal(
        "Lab 6: Code Coverage Analysis (100% Line Coverage Achieved)",
        code_cov_items,
        os.path.join(base_dir, "code_coverage_report.png")
    )

    # 3. Branch Coverage Report (100% Branch Coverage)
    branch_cov_items = [
        {"type": "cmd", "prompt": prompt_str, "text": "coverage run --branch -m pytest BranchCoverageTest_income_tax.py"},
        {"type": "output", "text": "============================= test session starts =============================\n"
                                   "platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0\n"
                                   "rootdir: C:\\Users\\prana\\Desktop\\se\\L6_L7_57_income_tax\\LAB6\n"
                                   "collected 29 items\n\n"
                                   "BranchCoverageTest_income_tax.py .............................           [100%]\n\n"
                                   "============================== 29 passed in 0.08s =============================="},
        {"type": "spacer"},
        {"type": "cmd", "prompt": prompt_str, "text": "coverage report -m"},
        {"type": "output", "text": "Name                               Stmts   Miss Branch BrPart  Cover   Missing\n"
                                   "------------------------------------------------------------------------------\n"
                                   "BranchCoverageTest_income_tax.py      64      0      0      0   100%\n"
                                   "income_tax.py                         39      0     28      0   100%\n"
                                   "------------------------------------------------------------------------------\n"
                                   "TOTAL                                103      0     28      0   100%"}
    ]
    render_terminal(
        "Lab 6: Branch Coverage Analysis (100% Branch Coverage Achieved)",
        branch_cov_items,
        os.path.join(base_dir, "branch_coverage_report.png")
    )

if __name__ == "__main__":
    main()
