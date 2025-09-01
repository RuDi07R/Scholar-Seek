Scholar-Seek: Academic Research Publication Analyzer
An intelligent web application that simplifies academic research by allowing users to search for publications and authors, and generate concise summaries of complex research papers using a transformer-based model.

🌟 Overview
Scholar-Seek addresses the challenge of information overload in academic research. It provides a simple interface to search for scholarly articles and authors via the Scholarly API and leverages a pre-trained BART model from Hugging Face to generate high-quality, abstractive summaries of the papers. This tool is designed to help students, researchers, and academics quickly identify and understand relevant literature in their field.

✨ Key Features
Author and Publication Search: Directly search for academic authors and their publications.

AI-Powered Summarization: Utilizes a transformer-based BART model for abstractive text summarization.

Performance Optimized: Implemented batching and caching to reduce latency by approximately 60% when processing large volumes of text.

Interactive Dashboard: A user-friendly interface built with Streamlit to display search results and summaries.

Basic Evaluation: Includes a keyword coverage metric to provide a basic evaluation of summary quality.

🛠️ Tech Stack
Backend: Python

Frontend: Streamlit

AI/ML: Hugging Face Transformers, PyTorch

Data Retrieval: Scholarly API

Core Libraries: Pandas, NLTK

🚀 Getting Started
Prerequisites
Python 3.10 or higher

pip for package management

Installation
Clone the repository:

```Bash

git clone https://github.com/YourUsername/Scholar-Seek.git
```
```Bash
cd Scholar-Seek
```
Create and activate a virtual environment:

```Bash

python -m venv venv
venv\Scripts\activate
```
Install the required packages:

```Bash

pip install -r requirements.txt
```
Running the Application
To launch the Streamlit app, run the following command in your terminal:

```Bash

streamlit run app.py
```
The application will open in your web browser.

🖼️ Screenshots
📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.
