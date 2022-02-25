from prettytable import PrettyTable


def generate_table(process):
    tables = []
    for p in process:
        table = PrettyTable()
        threads_name = []
        for t in p.threads:
            thread_info = []
            threads_name.append(t.name)
            thread_info.extend([f"pid: {t.tid}", f"priority: {p.priority}", f"state: {t.state}"])
            for i in t.instructions:
                thread_info.extend([f"name: {i.name}", f"state: {i.state}"])
            try:
                table.add_column(t.name, thread_info)
            except Exception as e:
                thread_info.extend(["-", "-"])
                table.add_column(t.name, thread_info)
        tables.append(table)
    return tables


def print_tables(tables):
    print("--------------------------\n")
    for t in tables:
        print(t)
        print()