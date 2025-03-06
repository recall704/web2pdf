import argparse
from playwright.sync_api import sync_playwright
from typing import Optional, Literal

def convert_to_pdf(
    url: str,
    output_path: str,
    format: Optional[Literal['Letter', 'Legal', 'Tabloid', 'Ledger', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']] = 'A4',
    scale: float = 1.0,
    margin_top: str = '0.5in',
    margin_right: str = '0.5in',
    margin_bottom: str = '0.5in',
    margin_left: str = '0.5in',
    print_background: bool = True,
    landscape: bool = False,
    viewport_width: int = 1200,
    viewport_height: int = 800,
    timeout: int = 30000,
    wait_for_network: bool = True,
    prefer_css_page_size: bool = True
):
    """Convert webpage to PDF with customizable options.

    Args:
        url: URL of the webpage to convert
        output_path: Path where to save the PDF file
        format: Page format (default: A4)
        scale: Scale of the webpage (default: 1.0)
        margin_top: Top margin (default: 0.5in)
        margin_right: Right margin (default: 0.5in)
        margin_bottom: Bottom margin (default: 0.5in)
        margin_left: Left margin (default: 0.5in)
        print_background: Whether to print background graphics (default: True)
        landscape: Whether to use landscape orientation (default: False)
        viewport_width: Width of the viewport (default: 1200)
        viewport_height: Height of the viewport (default: 800)
        timeout: Maximum time to wait for page load in milliseconds (default: 30000)
        wait_for_network: Whether to wait for network requests to complete (default: True)
        prefer_css_page_size: Whether to prefer page size from CSS @page (default: True)
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch()
        
        # Create new page with specified viewport
        page = browser.new_page(viewport={'width': viewport_width, 'height': viewport_height})
        
        # Emulate print media
        page.emulate_media(media='print')
        
        # Navigate to URL and wait for load
        page.goto(url, timeout=timeout, wait_until='networkidle' if wait_for_network else 'load')
        
        # Wait for fonts to load
        page.wait_for_load_state('networkidle')
        
        # Generate PDF with specified options
        page.pdf(
            path=output_path,
            format=format,
            scale=scale,
            margin={
                "top": margin_top,
                "right": margin_right,
                "bottom": margin_bottom,
                "left": margin_left
            },
            print_background=print_background,
            landscape=landscape,
            prefer_css_page_size=prefer_css_page_size
        )
        
        # Close browser
        browser.close()

def main():
    parser = argparse.ArgumentParser(description='Convert webpage to PDF using Playwright')
    parser.add_argument('-i', '--url', required=True, help='Input URL of the webpage')
    parser.add_argument('-o', '--output', required=True, help='Output PDF file path')
    parser.add_argument('--format', choices=['Letter', 'Legal', 'Tabloid', 'Ledger', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6'],
                        default='A4', help='Page format (default: A4)')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale of the webpage (default: 1.0)')
    parser.add_argument('--margin-top', default='0.5in', help='Top margin (default: 0.5in)')
    parser.add_argument('--margin-right', default='0.5in', help='Right margin (default: 0.5in)')
    parser.add_argument('--margin-bottom', default='0.5in', help='Bottom margin (default: 0.5in)')
    parser.add_argument('--margin-left', default='0.5in', help='Left margin (default: 0.5in)')
    parser.add_argument('--no-background', action='store_false', dest='print_background',
                        help='Do not print background graphics')
    parser.add_argument('--landscape', action='store_true', help='Use landscape orientation')
    parser.add_argument('--viewport-width', type=int, default=1200, help='Width of the viewport (default: 1200)')
    parser.add_argument('--viewport-height', type=int, default=800, help='Height of the viewport (default: 800)')
    parser.add_argument('--timeout', type=int, default=30000, help='Maximum time to wait for page load in milliseconds (default: 30000)')
    parser.add_argument('--no-wait-network', action='store_false', dest='wait_for_network',
                        help='Do not wait for network requests to complete')
    parser.add_argument('--no-prefer-css-page-size', action='store_false', dest='prefer_css_page_size',
                        help='Do not prefer page size from CSS @page')
    
    args = parser.parse_args()
    
    try:
        convert_to_pdf(
            args.url,
            args.output,
            format=args.format,
            scale=args.scale,
            margin_top=args.margin_top,
            margin_right=args.margin_right,
            margin_bottom=args.margin_bottom,
            margin_left=args.margin_left,
            print_background=args.print_background,
            landscape=args.landscape,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            timeout=args.timeout,
            wait_for_network=args.wait_for_network,
            prefer_css_page_size=args.prefer_css_page_size
        )
        print(f"Successfully converted {args.url} to {args.output}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
