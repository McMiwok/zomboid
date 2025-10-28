import datareader


if __name__ == "__main__":
    csv_reader = datareader.CsvDataReader()
    repo = datareader.ItemRepository(csv_reader)
    repo.load_data('items.csv')

    json_reader = datareader.JsonDataReader()
    repo_json = datareader.ItemRepository(json_reader)
    repo_json.load_data('items.json')

    print(repo.get_items_page(1, 3))