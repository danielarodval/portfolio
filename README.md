# Daniel Rodriguez Personal Development Overview

## Intro
I’ve always liked figuring out how things work under the hood, especially around dev ops, networking, and the tooling that keeps systems running. A lot of that started back in high school, learning Unix and NAS tooling in my CSIT courses and then in college hosting Minecraft on a Raspberry Pi to helping host hackathon projects, and it eventually turned into learning local deployment and self-hosted infrastructure more seriously.

Over time, that grew into an ongoing homelab where I test deployment workflows, reverse proxies, remote access, internal networking, and service architecture across different projects. Lately I’ve also been documenting the environment more intentionally with diagrams, service maps, and repo-level notes so the work is easier to follow than just “here’s a server I built.”

Contact me via [LinkedIn](https://www.linkedin.com/in/danielarodval/)
and/or check out [my portfolio website](https://www.danrodval.com/)

## README Content & Links

### Homelab Docs 🏠
- [Rack Diagram & Photos]()
- [Network Configuration]()
- [Deployment Pipeline]()
- [Website Structure]()

### Active Projects 🔄
- [Reverse Proxy Test](https://github.com/danielarodval/local-host-test-site)
  - Reverse Proxy, Containerization with Docker
  - Adding CI/CD tooling with GitHub using linked repo
- [Backend Testing for Full-Stack with Neon Postgres](https://github.com/danielarodval/backend-testing-neon-postgres)
  - Containerization with Docker, ORM Tooling
- [AMP Game Server Monitor](https://github.com/danielarodval/amp-monitor)
  - Full-Stack Deployment in Python with FastAPI, Neon Postgres, Reflex UI

### Upcoming Projects 👀
- Cluster Computing with Kubernetes
- Always Up VLLM Tooling with OpenClaw
- DNS Failover for Cloud Backup Hosted Sites

### Previous Projects ✅
- [Docusign AI Integration Hackathon](https://github.com/danielarodval/docusign-hackathon-2024)
  - Local LLM integration, Streamlit app, API integration, local/cloud hosting
- [Morningstar Webscraper & Visualizer](https://github.com/danielarodval/portfolio/tree/main/code_dir/Python/Selenium%20Morningstar%20Visualization)
  - Selenium Web-Scraper, Plotly Visualization,Financial Data Replication
- [U.S. Home Price Forecasting with 4 Multi-Variate Regression Techniques](https://github.com/danielarodval/portfolio/tree/main/code_dir/Python/Home%20Pricing%20Insights%20from%20Treasury%20and%20Index%20Funds)
  - Data Aggregation & Preparation, Hyperparameter Tuning, Regression Testing: Gradient Boosted, KNN, Random Forest, Linear Support Vector
  - Used 4 different data sources: Zillow, Morningstar Index Funds, U.S. Treasury Securities Holdings (SOMA)
- [Bin Packing Algorithm Testing](https://github.com/danielarodval/st-bin-packing)
  - Deployment via Streamlit, Network Flow & Bin Packing Testing
- [Machine Learning vs. Neural Network Clustering](https://github.com/danielarodval/portfolio/tree/main/code_dir/Python/Neural%20Network%20Attempt%20at%20Clustering)
  - PyTorch Testing, K-Nearest Neighbors Clustering,
- [JavaScript Website](https://github.com/danielarodval/js-site)
  - A Chakra UI website hosted on Vercel

## Rack Diagram & Photos

The server rack was created using an IKEA Eket cabinet alongside four 7U rails and a frame using 1x12 & 2x10 wood pieces that permit for roughly 10 inches of depth shared between front and back mounted devices.

All of the mounts were found online and modified using TinkerCAD for adding patches for ethernet as well as splitting the mount in two pieces due to 180mm 3D printer limitation.

![Rack Layout](images/rack-layout.svg)

## Network Configuration

Networking is configured via Unifi OS from Ubiquiti throughout the entire system. Ensuring device isolation and reducing data inflow/outflow points.

![Rack Layout](images/network-config.svg)

## Deployment Pipeline

Reverse proxy test was used as a proof of concept that is currently running online to ensure proper device isolation as well as docker container hosting with Cloudflare Tunnels. Can be seen on the following [test on danrodval-selfhosted](https://test.danrodval-selfhosted.com/) site.

![Rack Layout](images/deployment.svg)

## Website Structure

The intended layout/structure for the portfolio website is as follows:

1. rebasing home-pricing, nn vs. ml, and the webscraper onto streamlit webapps
2. containerizing said webapps
3. hosting them on respective subdomains on the portfolio site
4. ensuring dns failover for each linked site, wherein pings are sent to each streamlit alternative when the main site is reached to ensure running

![Rack Layout](images/web-structure.svg)