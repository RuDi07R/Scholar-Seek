import streamlit as st
from scholarly import scholarly
from collections import defaultdict
import time
from transformers import pipeline

def search_authors(author_name):
    search_query = scholarly.search_author(author_name)
    authors = []
    try:
        for _ in range(5):
            author = next(search_query)
            authors.append(author)
            time.sleep(0.1)
    except StopIteration:
        pass
    return authors

def get_author_publications(author):
    try:
        author = scholarly.fill(author, sections=["publications"])
        publications = author["publications"]
        author_details = {
            "name": author["name"],
            "affiliation": author.get("affiliation", "Unknown affiliation"),
            "num_publications": len(publications),
        }
        return publications, author_details
    except Exception as e:
        st.error(f"Error fetching publications: {str(e)}")
        return [], {}

def extract_year(pub):
    year = (
        pub.get("bib", {}).get("pub_year")
        or pub.get("bib", {}).get("year")
        or pub.get("year")
    )
    if not year and "citation" in pub:
        citation = pub["citation"]
        if isinstance(citation, str) and "," in citation:
            year = citation.split(",")[-1].strip()
    return str(year) if year else "Unknown"

def process_publications(publications):
    all_pubs = defaultdict(list)
    for pub in publications:
        year = extract_year(pub)
        title = pub.get("bib", {}).get("title", "Untitled")
        num_citations = pub.get("num_citations", 0)
        all_pubs[year].append((title, num_citations, pub))  # Store the entire pub object
    return all_pubs

def generate_summary(abstract):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    prompt = "Summarize this research paper: "
    input_text = prompt + abstract
    summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
    
    # Post-process the summary to ensure it starts with "This research paper discusses"
    if not summary.startswith("This research paper discusses"):
        summary = "This research paper discusses " + summary[0].lower() + summary[1:]
    
    return summary

def get_abstract(pub):
    filled_pub = scholarly.fill(pub)
    return filled_pub.get("bib", {}).get("abstract", "No abstract available")

def display_publications(all_pubs):
    st.subheader("Publications")
    for year, pubs in sorted(
        all_pubs.items(), reverse=True, key=lambda x: x[0] if x[0] != "Unknown" else "0"
    ):
        st.write(f"Year: {year}")
        pubs = sorted(pubs, key=lambda x: x[1], reverse=True)
        for index, (title, num_citations, pub) in enumerate(pubs):
            st.write(f"- {title} | {num_citations} citations")
            
            button_key = f"summary_button:{year}:{index}"
            summary_key = f"summary:{year}:{index}"
            
            if st.button(f"Show Summary", key=button_key):
                if summary_key not in st.session_state:
                    with st.spinner("Fetching abstract and generating summary..."):
                        abstract = get_abstract(pub)
                        summary = generate_summary(abstract)
                        st.session_state[summary_key] = summary
            
            if summary_key in st.session_state:
                st.info(st.session_state[summary_key])
        
        st.write("")

def main():
    st.set_page_config(page_title="Scholar Seek", page_icon="📚")
    st.title("Scholar Seek")

    with st.form(key='search_form'):        
        author_name = st.text_input("Enter professor's name:")
        submit_button = st.form_submit_button(label='Search')

    if submit_button or st.session_state.get("search", False):
        st.session_state["search"] = True

        if not author_name:
            st.warning("Please enter a professor's name.")
            return

        if "authors" not in st.session_state:
            with st.spinner("Searching for authors..."):
                authors = search_authors(author_name)
                st.session_state["authors"] = authors
        else:
            authors = st.session_state["authors"]

        if not authors:
            st.error("No authors found with that name.")
        
        elif len(authors) == 1:
            if "author_details" not in st.session_state or "all_pubs" not in st.session_state:
                st.success("Author found. Generating publication summary...")
                publications, author_details = get_author_publications(authors[0])
                all_pubs = process_publications(publications)
                st.session_state["author_details"] = author_details
                st.session_state["all_pubs"] = all_pubs

            # Display Author Summary
            st.subheader("Author Summary")
            st.write(f"**Name:** {st.session_state['author_details']['name']}")
            st.write(f"**Affiliation:** {st.session_state['author_details']['affiliation']}")
            st.write(f"**Number of Publications:** {st.session_state['author_details']['num_publications']}")

            display_publications(st.session_state["all_pubs"])

        else:
            options = [
                f"{author['name']} ({author.get('affiliation', 'Unknown affiliation')})"
                for author in authors
            ]
            selected_author = st.selectbox("Select the correct author:", options)

            if st.button("Generate Summary for Selected Author"):
                selected_index = options.index(selected_author)
                with st.spinner("Generating publication summary..."):
                    publications, author_details = get_author_publications(authors[selected_index])
                    all_pubs = process_publications(publications)
                    st.session_state["author_details"] = author_details
                    st.session_state["all_pubs"] = all_pubs

            if "author_details" in st.session_state and "all_pubs" in st.session_state:
                # Display Author Summary
                st.subheader("Author Summary")
                st.write(f"**Name:** {st.session_state['author_details']['name']}")
                st.write(f"**Affiliation:** {st.session_state['author_details']['affiliation']}")
                st.write(f"**Number of Publications:** {st.session_state['author_details']['num_publications']}")

                display_publications(st.session_state["all_pubs"])

if __name__ == "__main__":
    main()