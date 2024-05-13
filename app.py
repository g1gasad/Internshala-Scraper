from scripts.final import automation

def main():
    automation(posts_per_page=42, pages_to_scrape=7)
    
if __name__ == "__main__":
    main()