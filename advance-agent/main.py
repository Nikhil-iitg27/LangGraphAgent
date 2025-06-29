from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()


def main():
    workflow = Workflow()
    print("\n🧑‍🔬 Academic Research Discovery Agent\nType 'quit' or 'exit' to stop.")

    while True:
        query = input("\n🔍 Research Query (Field, Subtopic): ").strip()
        if query.lower() in {"quit", "exit"}:
            print("👋 Exiting. Goodbye!")
            break

        if query:
            # Validate query format: must contain a comma
            if ',' not in query or len(query.split(',')) != 2:
                print("⚠️  Please enter your query in the format: Field, Subtopic (e.g., Computer Science, Distributed Systems)")
                continue
            # Convert to the internal format expected by the workflow (Field -> Subtopic)
            field, subtopic = [x.strip() for x in query.split(',', 1)]
            formatted_query = f"{field} -> {subtopic}"
            result = workflow.run(formatted_query)
            print(f"\n📊 Results for: {field} -> {subtopic}")
            print("=" * 60)

            if result.error_logs:
                print("❗ Errors encountered:")
                for err in result.error_logs:
                    print(f"   - {err}")
                print("=" * 60)

            if result.advancements:
                print(f"\n🆕 Latest Advancements in {field} -> {subtopic}:")
                for i, adv in enumerate(result.advancements, 1):
                    print(f"\n{i}. 📄 {adv.title}")
                    if adv.authors:
                        print(f"   👥 Authors: {', '.join(adv.authors)}")
                    if adv.date:
                        print(f"   📅 Date: {adv.date}")
                    if adv.keywords:
                        print(f"   🏷️  Keywords: {', '.join(adv.keywords)}")
                    if adv.impact_statement:
                        print(f"   💡 Impact: {adv.impact_statement}")
                    if adv.language:
                        print(f"   🌐 Language: {adv.language}")
                    if adv.summary:
                        print(f"   📝 Summary: {adv.summary}")
                    if adv.paper_links:
                        print(f"   📚 Papers: {', '.join(str(link) for link in adv.paper_links)}")
                    if adv.blog_links:
                        print(f"   📰 Blogs: {', '.join(str(link) for link in adv.blog_links)}")
                    if adv.pdf_links:
                        print(f"   📄 PDFs: {', '.join(str(link) for link in adv.pdf_links)}")
                    if adv.code_links:
                        print(f"   💻 Code: {', '.join(str(link) for link in adv.code_links)}")
            else:
                print("⚠️  No advancements found for this query.")

            if result.synthesis:
                print("\n🔬 Synthesis & Trends:")
                print("-" * 40)
                print(result.synthesis)

            print("=" * 60)

if __name__ == "__main__":
    main()