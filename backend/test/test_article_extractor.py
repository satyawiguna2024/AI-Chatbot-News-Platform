import pytest
from app.services import ArticleExtractor, ArticleTranslator


@pytest.mark.asyncio
async def test_extract_article():
  extractor = ArticleExtractor()
  translator = ArticleTranslator()

  # url = "https://en.antaranews.com/news/431149/indonesias-mount-ciremai-fire-extinguished-after-burning-46-hectares"
  url = "https://en.antaranews.com/news/431145/brics-strength-must-bring-tangible-benefits-prabowo"
  article = await extractor.extract(url)
  
  translated = await translator.translate_to_indonesian(
    title=article.title,
    description=article.description,
    content=article.content
  )

  print("\n\n=== EXTRACTED ARTICLE ===")
  print(f"\nTitle       : {article.title}")
  print(f"\nDescription : {article.description}")
  print(f"\nAuthor      : {article.author}")
  print(f"\nPublished   : {article.published_at}")
  print(f"\nContent:\n{article.content}")
  
  # Translator Result
  print("\n\n=== ORIGINAL ===")
  print("\nORIGINAL TITLE: ", article.title)
  print("\nORIGINAL DESCRIPTION: ", article.description)
  print("\nORIGINAL CONTENT", article.content)
  
  print("\n\n=== TRANSLATED ===")
  print("\nTRANSLATED TITLE: ", translated.title)
  print("\nTRANSLATED DESCRIPTION: ", translated.description)
  print("\nTRANSLATED CONTENT: ", translated.content)

  assert article.title
  assert article.description
  assert article.content
  assert len(article.content) > 500
  
  assert translated.title
  assert translated.description
  assert translated.content
  
# Title                 : Indonesia's Mount Ciremai fire extinguished after burning 46 hectares
# Source                : Antaranews.com
# Author                : Prisca Triferna Violleta, Yashinta Difa
# Published             : 2026-09-12 22:56:10+00:00
# URL                   : https://en.antaranews.com/news/431149/indonesias-mount-ciremai-fire-extinguished-after-burning-46-hectares
# Description           : The Forestry Ministry, through the Mount Ciremai National Park Agency, confirmed on Saturday that a forest fire that burned 46.42 hectares of conservation ...
# Main Content Article  : Jakarta (ANTARA) - The Forestry Ministry, through the Mount Ciremai National Park Agency, confirmed on Saturday that a forest fire that burned 46.42 hectares of conservation area in West Java had bee… [+1540 chars]
# --------------------------------------------------------------------------------
# Title                 : BRICS strength must bring tangible benefits: Prabowo
# Source                : Antaranews.com
# Author                : Fathur Rochman, Raka Adji
# Published             : 2026-09-12 16:31:49+00:00
# URL                   : https://en.antaranews.com/news/431145/brics-strength-must-bring-tangible-benefits-prabowo
# Description           : President Prabowo Subianto emphasized that the collective strength of BRICS countries must be translated into tangible benefits for the public and strengthen ...
# Main Content Article  : Jakarta (ANTARA) - President Prabowo Subianto emphasized that the collective strength of BRICS countries must be translated into tangible benefits for the public and strengthen the voice of the Globa… [+1809 chars]
# --------------------------------------------------------------------------------
# Title                 : Last Night, a Star-studded Evening Celebrating Moncler’s Fifth Avenue Flagship Ushered in a New Chapter in the Brand’s Enduring Love Story With New York
# Source                : Antaranews.com
# Author                : PR Wire
# Published             : 2026-09-12 16:00:09+00:00
# URL                   : https://en.antaranews.com/news/431143/last-night-a-star-studded-evening-celebrating-monclers-fifth-avenue-flagship-ushered-in-a-new-chapter-in-the-brands-enduring-love-story-with-new-york
# Description           : -Last night, on occasion of the opening of Moncler&rsquo;s largest-ever global flagship on Fifth Avenue, special guests including Cher, Julia Roberts, Anne ...
# Main Content Article  : New York--(ANTARA/Business Wire)--Last night, on occasion of the opening of Moncler’s largest-ever global flagship on Fifth Avenue, special guests including Cher, Julia Roberts, Anne Hathaway, Serena… [+1781 chars]
# --------------------------------------------------------------------------------
# Title                 : Indonesia calls for stronger domestic resilience at the 18th BRICS
# Source                : Antaranews.com
# Author                : Maria Cicilia Galuh Prayudhia, Yashinta Difa
# Published             : 2026-09-12 15:47:04+00:00
# URL                   : https://en.antaranews.com/news/431140/indonesia-calls-for-stronger-domestic-resilience-at-the-18th-brics
# Description           : Indonesian President Prabowo Subianto called on BRICS member countries to strengthen domestic resilience and self-reliance, stressing that national ...
# Main Content Article  : Jakarta (ANTARA) - Indonesian President Prabowo Subianto called on BRICS member countries to strengthen domestic resilience and self-reliance, stressing that national sovereignty depends on a country… [+1902 chars]
# --------------------------------------------------------------------------------
# Title                 : Indonesia's fishery exports reach US$3 billion in first half of 2026
# Source                : Antaranews.com
# Author                : Shofi Ayudiana, Yashinta Difa
# Published             : 2026-09-12 15:45:20+00:00
# URL                   : https://en.antaranews.com/news/431136/indonesias-fishery-exports-reach-us3-billion-in-first-half-of-2026
# Description           : Indonesia recorded US$3 billion in fishery product exports during the first half of 2026, totaling 566,250 tons, as national quality certification efforts ...
# Main Content Article  : Jakarta (ANTARA) - Indonesia recorded US$3 billion in fishery product exports during the first half of 2026, totaling 566,250 tons, as national quality certification efforts helped expand access to g… [+1657 chars]
# --------------------------------------------------------------------------------
# Title                 : Indonesia intensifies forest fire response in six priority provinces
# Source                : Antaranews.com
# Author                : Hana Dewi, Raka Adji
# Published             : 2026-09-12 15:10:31+00:00
# URL                   : https://en.antaranews.com/news/431135/indonesia-intensifies-forest-fire-response-in-six-priority-provinces
# Description           : The National Disaster Mitigation Agency (BNPB) is continuing massive and integrated efforts to combat forest and land fires across six priority provinces as ...
# Main Content Article  : Jakarta (ANTARA) - The National Disaster Mitigation Agency (BNPB) is continuing massive and integrated efforts to combat forest and land fires across six priority provinces as dry conditions peak.The… [+2722 chars]
# --------------------------------------------------------------------------------
# Title                 : Prabowo highlights unity, Bandung spirit at BRICS Summit
# Source                : Antaranews.com
# Author                : Maria, Kenzu
# Published             : 2026-09-12 15:09:22+00:00
# URL                   : https://en.antaranews.com/news/431133/prabowo-highlights-unity-bandung-spirit-at-brics-summit
# Description           : President Prabowo Subianto invoked an Indonesian proverb to underscore the importance of unity in facing global challenges at the 2026 BRICS Summit in Bharat ...
# Main Content Article  : Jakarta (ANTARA) - President Prabowo Subianto invoked an Indonesian proverb to underscore the importance of unity in facing global challenges at the 2026 BRICS Summit in Bharat Mandapam, New Delhi, I… [+2214 chars]
# --------------------------------------------------------------------------------
# Title                 : BRICS plays key role in contributing to global resilience: Prabowo
# Source                : Antaranews.com
# Author                : Fathur, Kenzu
# Published             : 2026-09-12 14:29:11+00:00
# URL                   : https://en.antaranews.com/news/431132/brics-plays-key-role-in-contributing-to-global-resilience-prabowo
# Description           : President Prabowo Subianto said BRICS has an important role to play in strengthening collective capacity to contribute to global resilience.

# He made the ...
# Main Content Article  : Imagine what BRICS could achieve if this strength were fully mobilized to help secure food and energy supplies.
# Jakarta (ANTARA) - President Prabowo Subianto said BRICS has an important role to play… [+2618 chars]
# --------------------------------------------------------------------------------
# Title                 : Kemkomdigi tracks signals to find eight missing in Sunda Strait
# Source                : Antaranews.com
# Author                : Farhan Arda, Kuntum Khaira
# Published             : 2026-09-12 13:34:43+00:00
# URL                   : https://en.antaranews.com/news/431128/kemkomdigi-tracks-signals-to-find-eight-missing-in-sunda-strait
# Description           : The Ministry of Communication and Digital Affairs (Kemkomdigi) is working with mobile network operators and radio frequency monitoring offices to track ...
# Main Content Article  : Jakarta (ANTARA) - The Ministry of Communication and Digital Affairs (Kemkomdigi) is working with mobile network operators and radio frequency monitoring offices to track signals from devices belongi… [+2142 chars]
# --------------------------------------------------------------------------------
# Title                 : Prabowo affirms Indonesia's role at 18th BRICS Summit in New Delhi
# Source                : Antaranews.com
# Author                : Maria, Kenzu
# Published             : 2026-09-12 12:04:01+00:00
# URL                   : https://en.antaranews.com/news/431125/prabowo-affirms-indonesias-role-at-18th-brics-summit-in-new-delhi
# Description           : President Prabowo Subianto has affirmed Indonesia&#39;s active role in promoting multilateral cooperation and building strategic partnerships amid global ...
# Main Content Article  : Jakarta (ANTARA) - President Prabowo Subianto has affirmed Indonesia's active role in promoting multilateral cooperation and building strategic partnerships amid global dynamics through his participa… [+2000 chars]
# --------------------------------------------------------------------------------