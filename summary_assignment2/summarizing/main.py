from textcleaning import get_style_metrics
from summary_creator import hierarchical_style_summary, summarize_with_style,score_sentence
from utils import measure_length, chunk_text


def generate_query(content_summary, style_summary):

    return f"""Create a final summary that combines the content information with the writing style characteristics.

Content to summarize:
{content_summary}

Style to emulate:
{style_summary}

Please produce a coherent summary that:
1. Preserves the key information from the content
2. Matches the writing style characteristics
3. Maintains good readability and flow"""


def main():
    try:
        # Load input files
        with open(r"C:\Users\Asus\PycharmProjects\Mehrshad\summary_assignment2\data\content_text.txt", "r", encoding="utf-8") as f:
            content_text = f.read()

        with open(r"C:\Users\Asus\PycharmProjects\Mehrshad\summary_assignment2\data\style_text.txt", "r", encoding="utf-8") as f:
            style_text = f.read()

        # Get style characteristics
        style_metrics = get_style_metrics(style_text)


        total_context = 4000
        content_target = int(total_context * 0.8)
        style_target = total_context - content_target


        content_summary = hierarchical_style_summary(content_text, style_metrics, content_target)
        style_summary = hierarchical_style_summary(style_text, style_metrics, style_target)


        final_summary = summarize_with_style(content_summary, style_metrics)


        query = generate_query(content_summary, style_summary)


        with open(r"C:\Users\Asus\PycharmProjects\Mehrshad\summary_assignment2\data\styled_summary.txt", "w", encoding="utf-8") as f:
            f.write(final_summary)

        with open(r"C:\Users\Asus\PycharmProjects\Mehrshad\summary_assignment2\data\query.txt", "w", encoding="utf-8") as f:
            f.write(query)

        print("Successfully generated:")
        print(f"- styled_summary.txt ({measure_length(final_summary)} tokens)")
        print(f"- query.txt")

    except FileNotFoundError:
        print("Error: Input files not found. Please check file paths.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()