import random

# Defined Common Patterns in a dictionary as key value pair

# Keys represent functions like Variables, Loops

# Values are list where:

# 0th element is regex pattern

# 1st element is power query score

# 2nd element is pyspark score

# 3rd element is weightage (pending)

data = {

    "use of 'resident'(Can be done in Power Query)": [r"\bresident\b", 1, 0, random.randint(1, 5)],

    "concatenation(Can be done in Power Query)": [r"\bconcatenate\b", 1, 0, random.randint(1, 5)],

    "deprecated joins(Can be done in Pyspark)": [r"\bjoin\b", 0, 1, random.randint(1, 5)],

    "use of 'peek' or 'previous'(Can be done in Power Query)": [r"\bpeek\b|\bprevious\b", 1, 0, random.randint(1, 5)],

    "inline load(Can be done in Power Query)": [r"load\s+\*+\s*,?\s*\[?.*\]?\s+inline", 1, 0, random.randint(1, 5)],

    "autogenerate(Can be done in Power Query)": [r"\bautogenerate\b", 1, 0, random.randint(1, 5)],

    "Section Access(Can be done with RLS)": [r"SECTION\s+ACCESS", 1, 0, random.randint(1, 5)],

    "mapping load / applymap (Can be done in Power Query M joins)": [r"\bapplymap\b|\bmapping\s+load\b", 0, 1, random.randint(1, 5)],

    "Use of 'qualify' (Can be replaced with explicit renaming)": [r"\bqualify\b", 1, 0, random.randint(1, 5)],

    "Use of 'unqualify' (Avoid by managing naming explicitly)": [r"\bunqualify\b", 1, 0, random.randint(1, 5)],

    "loops: for/next or do/while (Can be avoided with transformations)": [r"\b(for\s+each|for\s+\w+|next|while|loop)\b", 0, 1, random.randint(1, 5)],

    "Use of variables for table names (Dynamic scripting)": [r"LET\s+\w+\s*=\s*['\"]?.+['\"]?;", 0, 1, random.randint(1, 5)],

    "Use of 'binary' load (Should be replaced with structured data sources)": [r"\bbinary\b", 0, 1, random.randint(1, 5)],

    "Use of 'store' command (Handled via data export pipelines)": [r"\bstore\b", 1, 0, random.randint(1, 5)],

    "Use of 'exit script' (Can be replaced with better conditional flow)": [r"\bexit\s+script\b", 1, 0, random.randint(1, 5)],

    "Use of temporary tables (Should be optimized or avoided)": [r"\btemp\b", 1, 0, random.randint(1, 5)],

    "Use of 'exists' function (Power Query supports anti/semi joins)": [r"\bexists\s*\(", 1, 0, random.randint(1, 5)],

    "Use of 'if', 'alt', 'null' expressions (Can be converted to M functions)": [r"\b(if|alt|null\()", 1, 0, random.randint(1, 5)],

    "Use of 'drop' statements (Manage table scopes in ETL)": [r"\bdrop\s+(table|fields?)\b", 0, 1, random.randint(1, 5)],

    "Use of 'noconcatenate' (Power Query handles this with explicit appends)": [r"\bnoConcatenate\b", 1, 0, random.randint(1, 5)],

    "Set analysis in load scripts (Should be handled in model or front-end)": [r"\b\{\$.*\}\b", 1, 0, random.randint(1, 5)],

    "Use of 'intervalmatch' (Can be replaced with range joins)": [r"\bintervalmatch\b", 0, 1, random.randint(1, 5)],

    "Use of 'generic load' (Better modeled with pivot/unpivot)": [r"\bgeneric\s+load\b", 0, 1, random.randint(1, 5)],

    "Field renaming (handled explicitly in Power Query)": [r"RENAME\s+FIELD", 1, 0, random.randint(1, 5)],

    "Loading from Excel or CSV (fully supported in Power Query)": [r"\bFROM\s+\[(.*\.xlsx|.*\.csv)\]", 1, 0, random.randint(1, 5)],

    "Join using 'inner', 'left', 'outer' keywords": [r"\b(inner|left|outer)\s+join\b", 1, 0, random.randint(1, 5)],

    "Date parsing or formatting": [r"\b(date#|timestamp#|date\(|timestamp\()", 1, 0, random.randint(1, 5)],

    "Nested if statements (map to M ‘if…then…else’)": [r"\bif\b.*\bthen\b.*\belse\b", 1, 0, random.randint(1, 5)],

    "Use of 'text' or 'num' formatting functions": [r"\btext\(|num\(", 1, 0, random.randint(1, 5)],

    "Cross-table transformations (handled via pivot/unpivot in Power Query)": [r"\bcrosstable\b", 1, 0, random.randint(1, 5)],

    "Group by aggregation logic": [r"\b(group\s+by|sum\(|avg\(|count\()", 1, 0, random.randint(1, 5)],

    "Composite keys created via '&' (replace with Power Query merge columns)": [r"\&", 1, 0, random.randint(1, 5)],

    "Manual date calendar generation (can use M functions or DAX calendar)": [r"\b(auto)?calendar\b", 1, 0, random.randint(1, 5)],

    "Dynamic field list loading using $(fields)": [r"\$\(fields?\)", 0, 1, random.randint(1, 5)],

    "Load balancing using loops": [r"\b(loop|for\s+each)\b.*load", 0, 1, random.randint(1, 5)],

    "Field aliasing using 'as'": [r"\bas\b", 1, 0, random.randint(1, 5)],

    "DATA REDUCTION in Section Access": [r"\bREDUCTION\b", 1, 0, random.randint(1, 5)],

    "Access control by USERID or GROUP": [r"\b(userid|group)\b", 1, 0, random.randint(1, 5)],

    #"Joins & Append (Multiple Concat)": [r"(?i)(Concatenate\s*(\(\s*\w+\s*\))?\s*LOAD[\s\S]+?(?=Concatenate|\Z))", 0, 1, random.randint(1, 5)]

}