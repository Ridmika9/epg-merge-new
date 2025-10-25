import requests

urls = [
    "https://epg.pw/api/epg.xml?channel_id=400477",
    "https://epg.pw/api/epg.xml?channel_id=400480",
    "https://epg.pw/api/epg.xml?channel_id=400479",
    "https://epg.pw/api/epg.xml?channel_id=400478",
    "https://epg.pw/api/epg.xml?channel_id=470446",
    "https://epg.pw/api/epg.xml?channel_id=470550",
    "https://epg.pw/api/epg.xml?channel_id=470888",
    "https://epg.pw/api/epg.xml?channel_id=470730",
    "https://epg.pw/api/epg.xml?channel_id=470390",
    "https://epg.pw/api/epg.xml?channel_id=453374",
    "https://epg.pw/api/epg.xml?channel_id=219100",
    "https://epg.pw/api/epg.xml?channel_id=219104",
    "https://epg.pw/api/epg.xml?channel_id=465006",
]

output_file = "merged_epg_new.xml"


def merge_epg(urls, output_file):
    print("📡 Downloading and merging EPG sources...")
    header_written = False
    total_channels = 0
    skipped = 0

    with open(output_file, "w", encoding="utf-8") as outfile:
        for url in urls:
            print(f"➡️ Fetching: {url}")
            try:
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                content = response.text.strip()

                # Clean XML header
                content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '').strip()

                if "<tv" in content and "</tv>" in content:
                    # Extract content inside <tv>...</tv>
                    inner = content.split("<tv", 1)[1].split(">", 1)[1].rsplit("</tv>", 1)[0]

                    if not header_written:
                        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n')
                        header_written = True

                    outfile.write(inner.strip() + "\n")
                    total_channels += 1
                else:
                    print(f"⚠️ Skipping malformed XML from: {url}")
                    skipped += 1

            except Exception as e:
                print(f"❌ Error fetching {url}: {e}")
                skipped += 1

        if header_written:
            outfile.write("</tv>\n")

    print(f"✅ Done! Merged EPG saved to '{output_file}'")
    print(f"📺 Total merged: {total_channels}, Skipped: {skipped}")


if __name__ == "__main__":
    merge_epg(urls, output_file)
