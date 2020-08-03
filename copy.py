import argparse
import json
import re

def main(json_path, export_json, open_tags):
    with open(json_path) as f:
       export_data = json.load(f)
    re_open_tags = "|".join(map(re.escape, open_tags))
    import_dict = extract(export_data, re_open_tags)
    with open(export_json, "w") as f:
        json.dump(import_dict, f, ensure_ascii=False)

def extract(export_data, re_open_tags):
    import_dict = {"pages": []}

    for page in export_data["pages"]:
        is_open = False
        for line in page["lines"]:
            if re.search(re_open_tags, line) is not None:
                is_open = True
                break
        if is_open:
            import_dict["pages"].append(page)
    return import_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inport_json')
    parser.add_argument('export_json')
    parser.add_argument('-t','--tags', nargs='+', default=["#open", "[open]"])
    args = parser.parse_args()
    main(args.inport_json, args.export_json, args.tags)