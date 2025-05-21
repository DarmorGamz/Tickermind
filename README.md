# Tickermind

<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
    <a href="#introduction">Getting Started</a>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#code-of-conduct">Code of Conduct</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
  </ol>
</details>

<!-- INTRODUCTION -->
## Introduction
<div align="center">
    <img src=".media/McMaster-logo.png" alt="Logo" width="200" height="100">
</div>
Welcome to our McMaster Engineering senior capstone project Tickermind: a Stock Scanner integrated with a local Large Language Model (LLM) for real-time sentiment analysis. This project aims to empower investors and traders by providing a tool that scans financial markets for stocks based on user-defined criteria and leverages advanced natural language processing to analyze market sentiment from news articles, social media, and other textual data sources. By running the LLM locally, the system ensures enhanced privacy, reduced latency, and independence from cloud-based services, making it a unique solution for real-time stock analysis in a fast-paced financial environment.   
<br><br>
The stock scanner combines robust data processing with cutting-edge AI to deliver actionable insights. It retrieves real-time market data using APIs, filters stocks based on technical indicators (e.g., moving averages, RSI), and applies sentiment analysis to gauge market perception of specific stocks. The local LLM processes unstructured text data to determine positive, negative, or neutral sentiment, providing a holistic view of a stock’s potential performance. Designed with scalability and user accessibility in mind, this project demonstrates the power of integrating AI with financial tools to support informed decision-making.

## Key Features
- **Real-Time Stock Scanning**: Filters stocks based on customizable technical indicators and fundamental metrics.
- **Local LLM Sentiment Analysis**: Analyzes news and social media text using a locally hosted LLM for privacy and performance.
- **User-Friendly Interface**: Intuitive dashboard for configuring scans and viewing sentiment-driven insights.
- **Extensible Architecture**: Modular design allows easy integration of additional data sources or analysis modules.
- **Privacy-Focused**: Local LLM processing eliminates dependency on external cloud services.

<!-- GETTING STARTED -->
## Getting Started

<!-- REQUIREMENTS -->
### Requirements

- Python 3.11.9

### Installation

#### Clone this repository
```bash
git clone https://github.com/DarmorGamz/Tickermind.git
```

#### Build the Docker image
```bash
docker compose up --build
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CODE OF CONDUCT -->
## Code of Conduct <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Growing%20Heart.png" alt="Growing Heart" style="width:1em; height:1em;" id="code-of-conduct" />

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on our code of conduct.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GPL License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Disclaimer -->
## Disclaimer <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Bomb.png" alt="Bomb" style="width:1em; height:1em;" id="disclaimer" />

This project is intended for educational purposes only. The content, scripts, and tools provided in this repository are for demonstration and learning purposes and should not be used for commercial or production environments without proper evaluation and adaptation.

The creators of this repository, Darren Morrison and Carter Glynn, are not responsible for any misuse, damage, or legal issues that may arise from using the code or concepts presented here. Users are advised to use the information and code at their own risk and discretion.

[contributors-shield]: https://img.shields.io/github/contributors/DarmorGamz/Tickermind.svg?style=for-the-badge
[contributors-url]: https://github.com/DarmorGamz/Tickermind/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DarmorGamz/Tickermind.svg?style=for-the-badge
[forks-url]: https://github.com/DarmorGamz/Tickermindm/network/members
[stars-shield]: https://img.shields.io/github/stars/DarmorGamz/Tickermind.svg?style=for-the-badge
[stars-url]: https://github.com/DarmorGamz/Tickermind/stargazers
[issues-shield]: https://img.shields.io/github/issues/DarmorGamz/Tickermind.svg?style=for-the-badge
[issues-url]: https://github.com/DarmorGamz/Tickermind/issues
[license-shield]: https://img.shields.io/github/license/DarmorGamz/Tickermind.svg?style=for-the-badge
[license-url]: https://github.com/DarmorGamz/Tickermind/blob/master/LICENSE.txt


<!-- Start Docker -->
<!-- docker compose up --build

<!-- Stop Docker -->
<!-- docker compose down -->

<!-- Debug Docker -->
<!-- docker compose logs -->
<!-- docker exec -it <container-name> /bin/bash -->
