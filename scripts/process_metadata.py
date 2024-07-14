import csv
import yaml
import os
from collections import OrderedDict, defaultdict

input_file_path = "infoscience-map.tsv"
output_dir = "../_data/elements"
order_file_path = "../_data/order.yml"

os.makedirs(output_dir, exist_ok=True)


class OrderedDumper(yaml.SafeDumper):
    pass


def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


OrderedDumper.add_representer(OrderedDict, _dict_representer)


def generate_yaml(data, index):
    indexes_values = [value.strip() for value in data.get("indexes", "").split(",")]
    range_values = [value.strip() for value in data.get("range_values", "").split(",")]
    filename = data.get("name", f"output_{index}")

    yaml_content = OrderedDict(
        [
            ("label", data.get("label", "")),
            ("label-fr", data.get("label-fr", "")),
            ("name", data.get("name", "")),
            ("schema", data.get("schema", "")),
            ("dc-element", data.get("dc-element", "")),
            ("dc-qualifier", data.get("dc-qualifier", "")),
            ("definition", data.get("definition", "")),
            ("obligation", data.get("obligation", "")),
            ("type", data.get("type", "")),
            ("repeatable", data.get("repeatable", "")),
            ("legacy_marc", data.get("legacy_marc", "")),
            (
                "indexes",
                [
                    OrderedDict(
                        [
                            ("configuration", data.get("configuration", "")),
                            ("indexes", indexes_values),
                        ]
                    )
                ],
            ),
            (
                "range",
                [
                    OrderedDict(
                        [
                            ("label", data.get("range_label", "")),
                            ("uri", data.get("range_url", "")),
                            ("values", range_values),
                        ]
                    )
                ],
            ),
        ]
    )

    output_file_path = os.path.join(output_dir, f"{filename}.yaml")

    with open(output_file_path, "w") as yaml_file:
        yaml.dump(
            yaml_content,
            yaml_file,
            Dumper=OrderedDumper,
            default_flow_style=False,
            allow_unicode=True,
        )


def generate_order_yaml(rows):
    order_dict = defaultdict(list)
    for row in rows:
        mtype = row.get("type", "undefined")
        name = row.get("name", "")
        order_dict[mtype].append(name)

    ordered_content = OrderedDict()
    for mtype, names in order_dict.items():
        ordered_content[mtype] = names

    with open(order_file_path, "w") as yaml_file:
        yaml.dump(
            ordered_content,
            yaml_file,
            Dumper=OrderedDumper,
            default_flow_style=False,
            allow_unicode=True,
        )


rows = []
with open(input_file_path, mode="r", encoding="utf-8") as file:
    tsv_reader = csv.DictReader(file, delimiter="\t")
    for index, row in enumerate(tsv_reader):
        rows.append(row)
        generate_yaml(row, index)

generate_order_yaml(rows)
