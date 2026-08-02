import zipfile
import xml.etree.ElementTree as ET


def extract_docx_table(path):

    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")

    root = ET.fromstring(xml)

    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    }

    rows = []

    for tr in root.findall(".//w:tr", ns):

        row = []

        for tc in tr.findall("./w:tc", ns):

            paragraphs = []

            for p in tc.findall("./w:p", ns):

                text = "".join(
                    t.text or ""
                    for t in p.findall(".//w:t", ns)
                ).strip()

                if text:
                    paragraphs.append(text)

            row.append(" ".join(paragraphs))

        if any(cell for cell in row):
            rows.append(row)

    return rows


def parse_hosts(path):

    rows = extract_docx_table(path)

    if len(rows) < 2:
        return []

    hosts = []

    for row in rows[1:]:

        if len(row) < 9:
            continue

        hosts.append({
            "OS": row[1],
            "DB": row[2],
            "Instances": " ".join(row[3].split()),
            "Window": row[5],
            "IP": row[6],
            "Segment": row[8]
        })

    return hosts