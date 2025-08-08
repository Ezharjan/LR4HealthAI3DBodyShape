import csv
import sys


# Read CSV file and extract data
def read_csv(file_name):
    data = []
    with open(file_name, "r", encoding="utf-8-sig") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            citation = {
                "Cites": row["Cites"],
                "Authors": row["Authors"],
                "Title": row["Title"],
                "Year": row["Year"],
                "Source": row["Source"],
                "ArticleURL": row["ArticleURL"],
                "Abstract": row["Abstract"],
            }
            data.append(citation)
    return data


# Sort data by the specified key
def sort_data(data, sort_by="Cites"):
    def convert_to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0  # Assign 0 if the value is not convertible to int

    return sorted(data, key=lambda x: convert_to_int(x[sort_by]), reverse=True)


# Convert data to Markdown format
def generate_markdown(data):
    markdown = ""
    for item in data:
        markdown += f"[{item['Title']}]({item['ArticleURL']})\n"
        markdown += f"  - **Authors:** {item['Authors']}\n"
        markdown += f"  - **Year:** {item['Year']}\n"
        markdown += f"  - **Cites:** {item['Cites']}\n"
        markdown += f"  - **Abstract:** {item['Abstract']}\n\n"
        markdown += f"<br> \n\n"
    return markdown


# Main program
def main():
    if len(sys.argv) < 2:
        print("Error: No CSV file specified.")
        print("Usage: python main.py <filename.csv>")
        print("Example: python main.py MR_Cites_03-23.csv")
        sys.exit(1)

    file_name = sys.argv[1]
    sort_by = input("Enter 'Cites' or 'Year' to sort by: ").strip()
    if sort_by not in ["Cites", "Year"]:
        sort_by = "Cites"

    try:
        data = read_csv(file_name)
        sorted_data = sort_data(data, sort_by)
        markdown_content = generate_markdown(sorted_data)

        # Set title and output file name based on sort type
        title = "### Sorted by Year" if sort_by == "Year" else "### Sorted by Citations"
        output_file_name = f"output_sort_by_{sort_by.lower()}.md"

        with open(output_file_name, "w", encoding="utf-8") as md_file:
            md_file.write(f"{title}\n\n")
            md_file.write(markdown_content)

        print(f"Markdown file '{output_file_name}' generated successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        print("Please ensure the CSV file exists in the same directory as this script.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()