import argparse
import sys
from datareader import CsvDataReader, ItemRepository, Item
from typing import Dict

PAGE_SIZE = 10
REPO = ItemRepository(CsvDataReader())
FILE_PATH = 'items.csv' 

try:
    REPO.load_data(FILE_PATH)
    if not REPO._items:
        print(f"Warning: File '{FILE_PATH}' is empty or contains no valid data.")
except Exception as e:
    print(f"Error loading data from {FILE_PATH}: {e}")
    sys.exit(1)


def print_item(item: Item):
    print(f"| ID: {item.id:<4} | Name: {item.name:<15} | Type: {item.type:<15} | Condition: {item.condition:<10} | Amount: {item.amount:>5} |")

def print_results(results: Dict[str, str], title: str):
    print(f"\n--- {title} ---")
    if not results:
        print("No data to display.")
        return
    for condition, percentage in results.items():
        print(f"  {condition:<10}: {percentage}")
    print("-------------------")


def handle_list(args):
    page_number = args.page
    page_size = args.size if args.size > 0 else PAGE_SIZE

    items_page = REPO.get_items_page(page_number, page_size)
    
    if not items_page:
        print(f"Page {page_number} is empty or does not exist.")
        return

    print(f"\n--- Page {page_number} (Size: {page_size}) ---")
    for item in items_page:
        print_item(item)
    print("-------------------------------------------------------------------")


def handle_get(args):
    item = REPO.get_item_by_id(args.id)
    if item:
        print("\n--- Found Item ---")
        print_item(item)
        print("-------------------------")
    else:
        print(f"Item with ID={args.id} not found.")


def handle_search(args):
    results = REPO.search_by_name(args.name)
    if results:
        print(f"\n--- Search Results for '{args.name}' ({len(results)} found) ---")
        for item in results:
            print_item(item)
        print("-------------------------------------------------------------------")
    else:
        print(f"No items found with name containing '{args.name}'.")


def handle_analyze_all(args):
    results = REPO.get_condition_percentage()
    print_results(results, "Condition Percentage Ratio for ALL Items")


def handle_analyze_name(args):
    results = REPO.get_condition_percentage_by_name(args.name)
    print_results(results, f"Condition Percentage Ratio for '{args.name}'")


def main():
    parser = argparse.ArgumentParser(
        description="CLI for managing and analyzing the survivors' item table.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(title='Available commands', dest='command')
    subparsers.required = True

    # Command 'list' (paginated output)
    # python cli.py list 1 --size 5
    list_parser = subparsers.add_parser('list', help='Display items page by page.')
    list_parser.add_argument('page', type=int, default=1, nargs='?', 
                             help='Page number for output (default: 1).')
    list_parser.add_argument('-s', '--size', type=int, default=PAGE_SIZE,
                             help=f'Page size (default: {PAGE_SIZE}).')
    list_parser.set_defaults(func=handle_list)

    # Command 'get' (search by ID)
    # python cli.py get 4
    get_parser = subparsers.add_parser('get', help='Retrieve item by ID.')
    get_parser.add_argument('id', type=int, help='Item ID.')
    get_parser.set_defaults(func=handle_get)

    # Command 'search' (search by name)
    # python cli.py search Nails
    search_parser = subparsers.add_parser('search', help='Search item by name.')
    search_parser.add_argument('name', type=str, help='Name or part of the item name.')
    search_parser.set_defaults(func=handle_search)

    # Command 'analyze-all' (condition analysis for all items)
    # python cli.py analyze-all
    analyze_all_parser = subparsers.add_parser('analyze-all', help='Get condition % ratio for all items.')
    analyze_all_parser.set_defaults(func=handle_analyze_all)

    # Command 'analyze-name' (condition analysis for a specific name)
    # python cli.py analyze-name Nails
    analyze_name_parser = subparsers.add_parser('analyze-name', help='Get condition % ratio for items of a specific name.')
    analyze_name_parser.add_argument('name', type=str, help='Item name for analysis.')
    analyze_name_parser.set_defaults(func=handle_analyze_name)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()