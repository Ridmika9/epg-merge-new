import requests

urls = [
    "https://epg.pw/api/epg.xml?channel_id=403626",
    "https://epg.pw/api/epg.xml?channel_id=400477",
    "https://epg.pw/api/epg.xml?channel_id=400480",
    "https://epg.pw/api/epg.xml?channel_id=405060",
    "https://epg.pw/api/epg.xml?channel_id=405134",
    "https://epg.pw/api/epg.xml?channel_id=400479",
    "https://epg.pw/api/epg.xml?channel_id=400478",
    "https://epg.pw/api/epg.xml?channel_id=405049",
    "https://epg.pw/api/epg.xml?channel_id=404833",
    "https://epg.pw/api/epg.xml?channel_id=405079",
    "https://epg.pw/api/epg.xml?channel_id=8821",
]

output_file = "epg.xml"

def merge_epg(urls, output_file):
    print("Downloading and merging EPG sources...")
    header_written = False

    with open(output_file, "w", encoding="utf-8") as outfile:
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                content = response.text

                # Remove XML declaration if present
                content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '').strip()

                if "<tv" in content and "</tv>" in content:
                    # Extract content inside <tv>...</tv>
                    inner = content.split("<tv")[1].split(">", 1)[1].rsplit("</tv>", 1)[0]

                    if not header_written:
                        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n')
                        header_written = True

                    outfile.write(inner.strip() + "\n")
                else:
                    print(f"⚠️ Skipping malformed XML from: {url}")
            except Exception as e:
                print(f"❌ Error fetching {url}: {e}")

        if header_written:
            outfile.write("</tv>\n")
    print(f"✅ Merged EPG saved to: {output_file}")

merge_epg(urls, output_file)
