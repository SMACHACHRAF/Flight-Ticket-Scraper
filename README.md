# Flight-Ticket-Scraper
A web application that scrapes flight tickets from a specific departure to a chosen destination using Selenium, BeautifulSoup, and an API. The extracted data, including flight details and prices, is cleaned, stored in MongoDB, and displayed in real-time for easy browsing and management.

# Web Scraping and Big Data Integration Project  
## Introduction  
This project was developed as part of the **Big Data** course and serves as a **Final Year Project (PFE)**. Its primary objective is to collect and analyze flight ticket data between specific destinations through **web scraping**, store the data in a **MongoDB** database, and build a **web application** for visualization and interaction.  

The project demonstrates the complete data lifecycle: from **data extraction** to **storage** and **web-based visualization**, focusing on the quality of data processing and ensuring scalability.  

## Web Scraping Methods  
We used **three distinct techniques** to extract data from online flight booking platforms:  
1. **Selenium:** For scraping dynamic and JavaScript-heavy websites requiring user interaction.  
2. **BeautifulSoup:** For parsing static pages with structured HTML content.  
3. **API Requests:** For direct data extraction from public APIs.  

## Data Storage  
The data is stored in **MongoDB**, a NoSQL database that efficiently handles large amounts of semi-structured data, enabling fast queries and integration with the web application.  

## Web Application Features  
- **Flight Ticket Display:** Users can browse flight tickets between selected destinations.  
- **Sorting and Filtering:** Data can be sorted and filtered based on price, date, and airline.  
- **Real-Time Updates:** Ensures up-to-date data by refreshing regularly.  
- **User Interaction:** Offers an intuitive and responsive design for seamless navigation.  

## Technologies Used  
- **Python** for data extraction and processing  
- **Selenium, BeautifulSoup, Requests** for scraping  
- **MongoDB** for storage  
- **Flask/Django** for the web application backend  
- **JavaScript, HTML, CSS** for front-end development  

## Project Architecture  
1. **Data Collection:** Multiple scraping methods for comprehensive data gathering.  
2. **Data Processing:** Clean and prepare the data for storage and visualization.  
3. **Data Storage:** Store the processed data in MongoDB for scalable access.  
4. **Web Application:** Display and interact with the data through a responsive web interface.  

## Future Improvements  
- Integrate more data sources to expand coverage.  
- Add advanced filtering, user authentication, and real-time alerts.  
- Use data visualization libraries (e.g., Plotly) for better insights.  
- Optimize scraping for faster and more efficient data extraction.  
