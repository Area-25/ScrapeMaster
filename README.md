# **ScrapeMaster**

---

# ScrapeMaster 🚀  
**Scrape entire websites, create LLM-ready datasets, and dominate the web.**  
We keep it raw and real—no API credits, just clever automation. 🤖  

---

## **What is ScrapeMaster?**
ScrapeMaster is your ultimate dataset generator:  
1. **Turn ideas into websites** with automated Google searches.  
2. Scrape and structure multi-layered websites into **LLM-ready JSONL files**.  
3. Keep things fun and transparent—no OpenAI or Google API keys needed.  

Built in **< 4 hours**, because that's the rule in **Area 25**. If it's not done by then, it's archived—no mercy.

---

## **How Does It Work?**
1. **You provide**:
   - How many websites you want (e.g., 3000).  
   - Topics in one of two ways:
     - Direct input: comma-separated list of topics
     - File input: .json, .yaml, .txt, or .md file containing topics

2. ScrapeMaster will:
   - Load your topics (from input or file)
   - Automate Google searches for those topics to find URLs
   - Scrape the websites, clean the data, and output **LLM-ready JSONL files**

---

## **Topic Input Formats**

### **1. Direct Input**
Use comma-separated topics directly in the command:
```bash
python scraper.py --websites 100 --topics "AI basics, machine learning, deep learning"
```

### **2. File Input**
Create a file with your topics in any of these formats:

#### JSON (topics.json)
```json
{
    "topics": [
        "AI basics",
        "machine learning",
        "deep learning"
    ]
}
```

#### YAML (topics.yaml)
```yaml
topics:
  - AI basics
  - machine learning
  - deep learning
```

#### Text (topics.txt)
```text
AI basics
machine learning
deep learning
```

#### Markdown (topics.md)
```markdown
- AI basics
- machine learning
- deep learning
```

Then run:
```bash
python scraper.py --websites 100 --topics topics.json
# or .yaml, .txt, .md
```

---

## **What if I Don't Know the Topics?**
We've got you covered! Use **ChatGPT** to brainstorm topics for your niche.  
Here's a **prompt template** to make it effortless:

> _"I am using a tool called ScrapeMaster to scrape websites for training an AI model. My main topic is [your niche]. Can you provide me a list of at least 30 detailed subtopics under this niche? Format the output as a markdown list with each topic on a new line starting with '-'. For example, if the niche is 'AI research,' include subtopics like 'deep learning for healthcare,' 'transformer architectures,' etc."_

Save ChatGPT's response directly as `topics.md` and you're ready to go!

---

## **Installation**
Clone this repo and install dependencies:
```bash
git clone https://github.com/Feel-The-AGI/ScrapeMaster.git
cd ScrapeMaster
pip install -r requirements.txt
```

---

## **Outputs**
- **`websites_master.json`**: Full list of URLs ScrapeMaster will process
- **`websites_completed.json`**: Successfully scraped and processed sites
- **`websites_errors.json`**: Failed sites (for retry)
- **`final_dataset/dataset.jsonl`**: Your final, LLM-ready dataset

---

## **Features**
1. **Flexible Topic Input**:
   - Direct command-line input or file-based input
   - Supports JSON, YAML, TXT, and MD formats

2. **Automated Topic Processing**:
   - Smart parsing of different file formats
   - Handles both simple lists and structured data

3. **Concurrent Google Searches**:
   - Multiple topics searched at once
   - Smart rate limiting to avoid blocks

4. **LLM-Ready Datasets**:
   - Clean, structured JSONL output
   - Ready for training or fine-tuning

5. **Fail-Safe Scraping**:
   - Tracks errors and progress
   - Resumes interrupted scraping
   - Detailed error logging

---

## **Limitations**
- Large datasets (e.g., 3000+ websites) can take time to process
- Google may throttle requests—use proxies or slower scraping speeds if needed
- Some websites may block scraping attempts (tracked in errors.json)

---

**Built by Feel-The-AGI in Area 25. Break rules. Build wonders. Finish in < 4 hours or archive it forever.**  