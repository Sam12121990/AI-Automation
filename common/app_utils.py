import re
from collections import Counter

class AppUtils:
    """
    A utility class for managing  helper functions

    used throughout the application.
    """

    def __init__(self):
        pass

    # Script analysis function with single key value pair

    @staticmethod
    def analyze_script_old(script_text, patterns):
        issues = []

        for feature, pattern in patterns.items():
            if re.search(pattern, script_text, re.IGNORECASE | re.DOTALL):
                issues.append(feature)
        return issues

    # Script analysis function with single key and multiple value defined in list

    @staticmethod
    def analyze_script(script_text, data):
        issues, pq_score, ps_score, pattern_match_count, regex_pattern, weightage = [], [], [], [], [], []

        for feature, value in data.items():
            pattern = value[0]

            if re.search(pattern, script_text, re.IGNORECASE | re.DOTALL):
                issues.append(feature)
                pq_score.append(value[1])
                ps_score.append(value[2])
                weightage.append(value[3])

                pattern_match_count.append(len(re.findall(pattern, script_text, re.IGNORECASE | re.DOTALL)))
                regex_pattern.append(pattern)

        return issues, pq_score, ps_score, pattern_match_count, regex_pattern, weightage

    @staticmethod
    def extract_data_connections(content):
        # Define the regex pattern to match ODBC and OLEDB connections

        pattern = r'(ODBC|OLEDB)\s+CONNECT\s+TO\s+\[([^\]]+)\]'

        # Find all matches in the content
        matches = re.findall(pattern, content)
        return matches

    @staticmethod
    def color_yes_no(val):
        if val == 'Yes':
            return 'color: green'

        elif val == 'No':
            return 'color: red'

        return ''

    @staticmethod
    def extract_join_append(content):
        # Pattern to match Concatenate ... LOAD blocks

        # concatenate_pattern = re.compile(r"(?i)(Concatenate\s*(?:\(\s*\w+\s*\))?\s*LOAD[\s\S]+?(?=Concatenate|$))")

        concatenate_pattern = re.compile(
            r"(?i)(?<!No)(Concatenate\s*(?:\(\s*\w+\s*\))?\s*LOAD[\s\S]+?(?=Concatenate|$))")

        # Pattern to match JOIN operations
        join_pattern = re.compile(r"(?i)(LEFT JOIN|INNER JOIN|RIGHT JOIN)\s*\((\w+)\)")

        # Find all Concatenate ... LOAD blocks
        concatenate_blocks = concatenate_pattern.findall(content)

        # Count Resident table usage in Concatenate ... LOAD blocks
        resident_counter = Counter()

        for block in concatenate_blocks:
            match = re.search(r"Resident\s+(\w+)", block, re.IGNORECASE)

            if match:
                resident_table = match.group(1)
                resident_counter[resident_table] += 1

        # Count JOIN operations for each table
        join_counter = Counter()
        join_details = {}

        for match in join_pattern.finditer(content):
            join_type = match.group(1).upper()
            table_name = match.group(2)

            join_counter[(table_name, join_type)] += 1

            if table_name not in join_details:
                join_details[table_name] = Counter()

            join_details[table_name][join_type] += 1

        return join_details, resident_counter

    @staticmethod
    def calculate_total_resident_and_joins(resident_details, join_details):
        total_joins, total_resident = 0, 0

        for table, count in resident_details.items():
            if table in join_details:
                total_resident += count

                total_joins += sum(join_details[table].values())
        return total_resident, total_joins